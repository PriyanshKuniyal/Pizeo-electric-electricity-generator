import asyncio
import json
import csv
import os
import re
from datetime import datetime
from typing import Optional, Dict, Any, List
import serial
import serial.tools.list_ports
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Piezoelectric Energy Dashboard")

# Global variables
serial_connection: Optional[serial.Serial] = None
connected_websockets: List[WebSocket] = []
is_logging = False
csv_file_path = None
csv_writer = None
csv_file = None

class SerialData(BaseModel):
    voltage: float
    energy: float
    steps: int
    power: float
    led: str
    timestamp: str

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if self.active_connections:
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending to WebSocket: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for connection in disconnected:
                self.disconnect(connection)

manager = ConnectionManager()

def parse_sensor_data(raw_data: str) -> Optional[Dict[str, Any]]:
    """Parse the raw sensor data string into structured data"""
    try:
        lines = raw_data.strip().split('\n')
        data = {}
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('-'):
                continue
                
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == 'voltage':
                    data['voltage'] = float(value)
                elif key == 'energy':
                    data['energy'] = float(value)
                elif key == 'steps':
                    data['steps'] = int(value)
                elif key == 'power':
                    data['power'] = float(value)
                elif key == 'led':
                    data['led'] = value.upper()
        
        if len(data) >= 5:  # Ensure we have all required fields
            data['timestamp'] = datetime.now().isoformat()
            return data
    except Exception as e:
        logger.error(f"Error parsing sensor data: {e}")
    
    return None

def setup_csv_logging():
    """Setup CSV file for data logging"""
    global csv_file_path, csv_writer, csv_file
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file_path = f"data/piezo_data_{timestamp}.csv"
    
    csv_file = open(csv_file_path, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['timestamp', 'voltage', 'energy', 'steps', 'power', 'led'])
    csv_file.flush()
    
    logger.info(f"CSV logging started: {csv_file_path}")

def log_to_csv(data: Dict[str, Any]):
    """Log data to CSV file"""
    global csv_writer, csv_file
    
    if csv_writer and is_logging:
        try:
            csv_writer.writerow([
                data['timestamp'],
                data['voltage'],
                data['energy'],
                data['steps'],
                data['power'],
                data['led']
            ])
            csv_file.flush()
        except Exception as e:
            logger.error(f"Error writing to CSV: {e}")

def close_csv_logging():
    """Close CSV file"""
    global csv_file, csv_writer
    
    if csv_file:
        csv_file.close()
        csv_file = None
        csv_writer = None
        logger.info("CSV logging stopped")

async def read_serial_data():
    """Continuously read data from serial port"""
    global serial_connection
    
    buffer = ""
    
    while serial_connection and serial_connection.is_open:
        try:
            if serial_connection.in_waiting > 0:
                chunk = serial_connection.read(serial_connection.in_waiting).decode('utf-8')
                buffer += chunk
                
                # Look for complete data blocks (ending with dashes)
                if '------------------------------' in buffer:
                    parts = buffer.split('------------------------------')
                    for part in parts[:-1]:  # Process all complete parts
                        if part.strip():
                            parsed_data = parse_sensor_data(part)
                            if parsed_data:
                                # Broadcast to all connected clients
                                await manager.broadcast(parsed_data)
                                
                                # Log to CSV if logging is enabled
                                if is_logging:
                                    log_to_csv(parsed_data)
                    
                    # Keep the incomplete part in buffer
                    buffer = parts[-1]
            
            await asyncio.sleep(0.01)  # Small delay to prevent busy waiting
            
        except Exception as e:
            logger.error(f"Error reading serial data: {e}")
            break

@app.get("/")
async def get_dashboard():
    """Serve the main dashboard HTML"""
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/ports")
async def get_available_ports():
    """Get list of available serial ports"""
    try:
        ports = serial.tools.list_ports.comports()
        port_list = [{"device": port.device, "description": port.description} for port in ports]
        return {"ports": port_list}
    except Exception as e:
        logger.error(f"Error getting ports: {e}")
        return {"ports": []}

class SerialConnectRequest(BaseModel):
    port: str
    baudrate: int = 9600

@app.post("/api/connect")
async def connect_serial(request: SerialConnectRequest):
    """Connect to serial port"""
    global serial_connection
    
    try:
        if serial_connection and serial_connection.is_open:
            serial_connection.close()
        
        serial_connection = serial.Serial(request.port, request.baudrate, timeout=1)
        
        # Start reading data in background
        asyncio.create_task(read_serial_data())
        
        return {"status": "connected", "port": request.port, "baudrate": request.baudrate}
    
    except Exception as e:
        logger.error(f"Error connecting to serial port: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/disconnect")
async def disconnect_serial():
    """Disconnect from serial port"""
    global serial_connection
    
    try:
        if serial_connection and serial_connection.is_open:
            serial_connection.close()
            serial_connection = None
        return {"status": "disconnected"}
    
    except Exception as e:
        logger.error(f"Error disconnecting: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/logging/start")
async def start_logging():
    """Start CSV logging"""
    global is_logging
    
    try:
        if not is_logging:
            setup_csv_logging()
            is_logging = True
        return {"status": "logging_started", "file": csv_file_path}
    
    except Exception as e:
        logger.error(f"Error starting logging: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/logging/stop")
async def stop_logging():
    """Stop CSV logging"""
    global is_logging
    
    try:
        is_logging = False
        close_csv_logging()
        return {"status": "logging_stopped"}
    
    except Exception as e:
        logger.error(f"Error stopping logging: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/status")
async def get_status():
    """Get current system status"""
    return {
        "serial_connected": serial_connection is not None and serial_connection.is_open,
        "logging": is_logging,
        "csv_file": csv_file_path if is_logging else None,
        "websocket_connections": len(manager.active_connections)
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

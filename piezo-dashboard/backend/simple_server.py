import asyncio
import json
import csv
import os
import re
import http.server
import socketserver
import threading
import urllib.parse
import random
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
import serial
import serial.tools.list_ports
import websockets
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
serial_connection: Optional[serial.Serial] = None
connected_websockets: List = []
is_logging = False
csv_file_path = None
csv_writer = None
csv_file = None
dummy_data_enabled = False
dummy_data_task = None

# Dummy data simulation state
dummy_state = {
    'voltage': 2.5,
    'steps': 0,
    'led': 'OFF',
    'last_update': time.time()
}

def check_dummy_data_enabled():
    """Check if dummy data file exists"""
    return os.path.exists('dummy_data.cfg')

async def generate_dummy_data():
    """Generate realistic dummy data continuously with smooth transitions"""
    global dummy_state
    
    logger.info("🎭 Dummy data generator started - Delete dummy_data.cfg to stop")
    
    while check_dummy_data_enabled():
        try:
            # Simulate voltage spikes (like piezo presses) - 20% chance
            if random.random() < 0.20:
                # Sharp spike to simulate press
                dummy_state['voltage'] = random.uniform(3.5, 4.8)
                dummy_state['steps'] += 1
                dummy_state['led'] = 'ON'
            else:
                # Gradual decay back to baseline
                dummy_state['voltage'] *= 0.85  # Fast decay
                dummy_state['voltage'] += random.uniform(-0.1, 0.1)  # Small noise
                dummy_state['voltage'] = max(0.1, min(5.0, dummy_state['voltage']))
                
                # Turn off LED after spike
                if dummy_state['voltage'] < 1.0:
                    dummy_state['led'] = 'OFF'
            
            # Calculate energy and power based on voltage
            energy = dummy_state['voltage'] * dummy_state['voltage'] * 0.0001
            power = dummy_state['voltage'] * dummy_state['voltage'] * 0.001
            power = max(0, power)
            
            # Create data packet
            data = {
                'timestamp': datetime.now().isoformat(),
                'voltage': round(dummy_state['voltage'], 3),  # 3 decimals for smooth display
                'energy': round(energy, 6),
                'steps': dummy_state['steps'],
                'power': round(power, 5),
                'led': dummy_state['led']
            }
            
            # Broadcast to all connected clients immediately
            await broadcast_to_websockets(data)
            
            # Log to CSV if logging is enabled
            if is_logging:
                log_to_csv(data)
            
            # Fast update rate: 100ms (10 updates per second) for smooth animation
            await asyncio.sleep(0.1)
            
        except Exception as e:
            logger.error(f"Error in dummy data generator: {e}")
            await asyncio.sleep(1)
    
    logger.info("🎭 Dummy data generator stopped - File deleted or disabled")

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
    
    if not os.path.exists("../data"):
        os.makedirs("../data")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file_path = f"../data/piezo_data_{timestamp}.csv"
    
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

async def broadcast_to_websockets(data):
    """Broadcast data to all connected WebSocket clients"""
    if connected_websockets:
        disconnected = []
        for websocket in connected_websockets:
            try:
                await websocket.send(json.dumps(data))
            except Exception as e:
                logger.error(f"Error sending to WebSocket: {e}")
                disconnected.append(websocket)
        
        # Remove disconnected clients
        for websocket in disconnected:
            if websocket in connected_websockets:
                connected_websockets.remove(websocket)

async def read_serial_data():
    """Continuously read data from serial port with minimal latency"""
    global serial_connection
    
    buffer = ""
    
    while serial_connection and serial_connection.is_open:
        try:
            if serial_connection.in_waiting > 0:
                chunk = serial_connection.read(serial_connection.in_waiting).decode('utf-8', errors='ignore')
                buffer += chunk
                
                # Look for complete data blocks (ending with dashes or newlines)
                if '-------' in buffer or buffer.count('\n') >= 5:
                    parts = buffer.split('-------')
                    for part in parts[:-1]:  # Process all complete parts
                        if part.strip():
                            parsed_data = parse_sensor_data(part)
                            if parsed_data:
                                # Broadcast immediately - no buffering
                                await broadcast_to_websockets(parsed_data)
                                
                                # Log to CSV if logging is enabled
                                if is_logging:
                                    log_to_csv(parsed_data)
                    
                    # Keep the incomplete part in buffer
                    buffer = parts[-1]
            
            # Ultra-short delay for instant response (1ms)
            await asyncio.sleep(0.001)
            
        except Exception as e:
            logger.error(f"Error reading serial data: {e}")
            break

async def websocket_handler(websocket, path):
    """Handle WebSocket connections"""
    connected_websockets.append(websocket)
    logger.info(f"WebSocket connected. Total connections: {len(connected_websockets)}")
    
    try:
        async for message in websocket:
            # Handle incoming messages if needed
            pass
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(connected_websockets)}")

class DashboardHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler for the dashboard"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="../frontend", **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path.startswith('/static/'):
            # Remove /static/ prefix since files are in frontend folder
            self.path = self.path.replace('/static/', '/')
        elif self.path == '/api/ports':
            self.send_api_response(self.get_available_ports())
            return
        elif self.path == '/api/status':
            self.send_api_response(self.get_status())
            return
        
        super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/connect':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            self.send_api_response(self.connect_serial(data))
        elif self.path == '/api/disconnect':
            self.send_api_response(self.disconnect_serial())
        elif self.path == '/api/logging/start':
            self.send_api_response(self.start_logging())
        elif self.path == '/api/logging/stop':
            self.send_api_response(self.stop_logging())
        else:
            super().do_POST()
    
    def send_api_response(self, data):
        """Send JSON API response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def get_available_ports(self):
        """Get list of available serial ports"""
        try:
            ports = serial.tools.list_ports.comports()
            port_list = [{"device": port.device, "description": port.description} for port in ports]
            return {"ports": port_list}
        except Exception as e:
            logger.error(f"Error getting ports: {e}")
            return {"ports": []}
    
    def connect_serial(self, data):
        """Connect to serial port"""
        global serial_connection, dummy_data_task
        
        try:
            if serial_connection and serial_connection.is_open:
                serial_connection.close()
            
            port = data.get('port')
            baudrate = data.get('baudrate', 9600)
            
            serial_connection = serial.Serial(port, baudrate, timeout=1)
            
            # Stop dummy data when real connection is made
            if dummy_data_task and not dummy_data_task.done():
                logger.info("🔌 Real sensor connected - stopping dummy data")
                dummy_data_task.cancel()
            
            # Start reading data in background
            asyncio.create_task(read_serial_data())
            
            return {"status": "connected", "port": port, "baudrate": baudrate}
        
        except Exception as e:
            logger.error(f"Error connecting to serial port: {e}")
            return {"status": "error", "message": str(e)}
    
    def disconnect_serial(self):
        """Disconnect from serial port"""
        global serial_connection
        
        try:
            if serial_connection and serial_connection.is_open:
                serial_connection.close()
                serial_connection = None
            return {"status": "disconnected"}
        
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
            return {"status": "error", "message": str(e)}
    
    def start_logging(self):
        """Start CSV logging"""
        global is_logging
        
        try:
            if not is_logging:
                setup_csv_logging()
                is_logging = True
            return {"status": "logging_started", "file": csv_file_path}
        
        except Exception as e:
            logger.error(f"Error starting logging: {e}")
            return {"status": "error", "message": str(e)}
    
    def stop_logging(self):
        """Stop CSV logging"""
        global is_logging
        
        try:
            is_logging = False
            close_csv_logging()
            return {"status": "logging_stopped"}
        
        except Exception as e:
            logger.error(f"Error stopping logging: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_status(self):
        """Get current system status"""
        return {
            "serial_connected": serial_connection is not None and serial_connection.is_open,
            "logging": is_logging,
            "csv_file": csv_file_path if is_logging else None,
            "websocket_connections": len(connected_websockets)
        }
    
    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_http_server():
    """Start the HTTP server"""
    PORT = 8888
    with socketserver.TCPServer(("", PORT), DashboardHTTPHandler) as httpd:
        logger.info(f"HTTP server serving at port {PORT}")
        logger.info(f"Dashboard available at: http://localhost:{PORT}")
        httpd.serve_forever()

def start_websocket_server():
    """Start the WebSocket server"""
    return websockets.serve(websocket_handler, "localhost", 8889)

async def main():
    """Main function to start both servers"""
    global dummy_data_task
    
    # Start WebSocket server
    websocket_server = await start_websocket_server()
    logger.info("WebSocket server started on port 8889")
    
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    # Check if dummy data should be enabled
    if check_dummy_data_enabled():
        logger.info("🎭 Dummy data mode enabled - generating simulated data")
        logger.info("📝 Delete 'dummy_data.cfg' file to stop dummy data and use real sensors")
        dummy_data_task = asyncio.create_task(generate_dummy_data())
    else:
        logger.info("📡 Real sensor mode - connect via Bluetooth/Serial")
    
    # Periodically check if dummy data file status changed
    async def check_dummy_status():
        global dummy_data_task
        last_status = check_dummy_data_enabled()
        
        while True:
            await asyncio.sleep(2)  # Check every 2 seconds
            current_status = check_dummy_data_enabled()
            
            if current_status != last_status:
                if current_status:
                    logger.info("🎭 Dummy data enabled - starting generator")
                    dummy_data_task = asyncio.create_task(generate_dummy_data())
                else:
                    logger.info("📡 Dummy data disabled - switched to real sensor mode")
                    if dummy_data_task:
                        dummy_data_task.cancel()
                
                last_status = current_status
    
    # Start the status checker
    asyncio.create_task(check_dummy_status())
    
    # Keep the WebSocket server running
    await websocket_server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down servers...")
        if serial_connection and serial_connection.is_open:
            serial_connection.close()
        if is_logging:
            close_csv_logging()

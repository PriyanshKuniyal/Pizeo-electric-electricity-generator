# 🔋 Piezoelectric Energy Harvesting Dashboard

A **real-time web application** that displays live sensor data from a Raspberry Pi piezoelectric energy generator via Bluetooth/Serial communication. Perfect for science fair demonstrations and educational projects.

![Dashboard Preview](https://img.shields.io/badge/Status-Ready%20to%20Use-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--time-orange)

## ✨ Features

### 🔄 Real-time Data Display
- **Live Metrics**: Voltage, Energy, Steps, Power, LED Status
- **Smooth Graphs**: Continuously updating voltage graph (60-second window)
- **WebSocket Integration**: Instant updates with no refresh delays
- **Responsive Design**: Modern dark theme with animated cards

### 📊 Data Visualization
- **Real-time Chart**: Voltage vs Time with smooth animations
- **Color-coded Metrics**: Each metric has its own color scheme
- **LED Status Indicator**: Visual ON/OFF indicator with glowing effects
- **Interactive UI**: Hover effects and smooth transitions

### 💾 Data Logging
- **CSV Export**: Timestamped data logging to CSV files
- **Start/Stop Controls**: Toggle logging from the web interface
- **Auto-timestamping**: All data points include precise timestamps
- **File Management**: Organized data storage in `/data` folder

### 🔌 Communication
- **Serial/Bluetooth**: Supports COM ports and Bluetooth connections
- **Auto Port Detection**: Lists available serial ports automatically
- **Configurable Baud Rate**: Support for various communication speeds
- **Error Handling**: Robust connection management with reconnection

## 🚀 Quick Start

### Prerequisites
- **Python 3.7+**
- **Raspberry Pi** with Bluetooth/Serial capability
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone/Download the project**:
   ```bash
   cd "d:/Github models/Pizeo-electric-electricity-generator/piezo-dashboard"
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   python backend/main.py
   ```

4. **Open your browser**:
   ```
   http://localhost:8000
   ```

## 📡 Raspberry Pi Data Format

Your Raspberry Pi should send data in this format over Bluetooth/Serial:

```
Voltage: 2.84
Energy: 0.000404
Steps: 12
Power: 0.00007
LED: ON

------------------------------
```

### Communication Settings
- **Baud Rate**: 9600 (default) or configurable
- **Data Rate**: ~0.5 seconds per reading (2 Hz)
- **Protocol**: Plain text over serial/Bluetooth
- **Terminator**: `------------------------------`

## 🎯 Usage Guide

### 1. **Connect to Raspberry Pi**
   - Click "🔄" to refresh available serial ports
   - Select your Bluetooth COM port (e.g., COM3, COM4)
   - Choose the correct baud rate (usually 9600)
   - Click "Connect"

### 2. **Monitor Real-time Data**
   - Watch live metrics update automatically
   - Observe the voltage graph for trends
   - Check LED status indicator
   - Monitor connection status in the header

### 3. **Data Logging**
   - Click "Start Logging" to begin CSV recording
   - Data is saved to `data/piezo_data_YYYYMMDD_HHMMSS.csv`
   - Click "Stop Logging" when finished
   - Files include all sensor readings with timestamps

### 4. **Graph Controls**
   - **Clear Graph**: Reset the voltage chart
   - **Auto-scaling**: Y-axis adjusts to data range
   - **Zoom**: Mouse wheel to zoom in/out
   - **Pan**: Click and drag to navigate

## 🛠️ Customization

### Modify Data Format
Edit `parse_sensor_data()` in `backend/main.py`:

```python
def parse_sensor_data(raw_data: str) -> Optional[Dict[str, Any]]:
    # Customize parsing logic here
    # Add new sensor types or change format
```

### Adjust Graph Settings
Modify `setupChart()` in `frontend/app.js`:

```javascript
realtime: {
    duration: 60000, // Change time window (ms)
    refresh: 500,    // Update rate (ms)
    // ... other settings
}
```

### Change Color Scheme
Edit CSS variables in `frontend/styles.css`:

```css
.voltage-card { background: rgba(255, 215, 0, 0.1); }  /* Yellow */
.energy-card { background: rgba(74, 144, 226, 0.1); }   /* Blue */
.steps-card { background: rgba(26, 188, 156, 0.1); }    /* Cyan */
.power-card { background: rgba(255, 165, 0, 0.1); }     /* Orange */
```

## 📁 Project Structure

```
piezo-dashboard/
├── backend/
│   └── main.py              # FastAPI server + WebSocket + Serial
├── frontend/
│   ├── index.html          # Main dashboard HTML
│   ├── styles.css          # Dark theme + animations
│   └── app.js              # Real-time chart + WebSocket client
├── data/                   # CSV log files (auto-created)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard page |
| `/api/ports` | GET | List available serial ports |
| `/api/connect` | POST | Connect to serial port |
| `/api/disconnect` | POST | Disconnect from serial port |
| `/api/logging/start` | POST | Start CSV logging |
| `/api/logging/stop` | POST | Stop CSV logging |
| `/api/status` | GET | Get system status |
| `/ws` | WebSocket | Real-time data stream |

## 🐛 Troubleshooting

### Serial Connection Issues
- **Port not found**: Check if Raspberry Pi is paired and connected
- **Permission denied**: Run as administrator (Windows) or check permissions (Linux/Mac)
- **Data not appearing**: Verify baud rate and data format

### WebSocket Problems
- **No real-time updates**: Check browser console for WebSocket errors
- **Frequent disconnections**: Ensure stable network connection
- **Performance issues**: Reduce update frequency in code

### Bluetooth Setup (Windows)
1. Pair your Raspberry Pi in Windows Bluetooth settings
2. Check "More Bluetooth options" → "COM Ports" tab
3. Note the outgoing COM port number (e.g., COM3)
4. Use this port in the dashboard

## 🎓 Educational Value

Perfect for demonstrating:
- **Energy harvesting concepts**
- **Real-time data acquisition**
- **IoT communication protocols**
- **Web-based monitoring systems**
- **Data visualization techniques**

## 📊 Sample Data

```csv
timestamp,voltage,energy,steps,power,led
2025-11-08T15:30:45.123456,2.84,0.000404,12,0.00007,ON
2025-11-08T15:30:45.623456,2.91,0.000421,13,0.00008,ON
2025-11-08T15:30:46.123456,2.78,0.000389,14,0.00006,OFF
```

## 🤝 Contributing

Feel free to enhance this project:
- Add new sensor types
- Improve the UI/UX
- Add data export options
- Implement alerts/notifications
- Add historical data analysis

## 📄 License

This project is open-source and available under the MIT License.

---

**🔬 Built for Science Fair Excellence! ⚡**

*Demonstrate the power of piezoelectric energy harvesting with real-time, professional-grade monitoring.*

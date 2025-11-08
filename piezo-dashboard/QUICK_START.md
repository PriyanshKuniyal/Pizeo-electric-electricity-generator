# 🎯 Dashboard Quick Start Guide

## Current Status
Your dashboard is now **fully functional** and matches your reference design exactly!

## What You See
✅ **Clean Interface** - Just the essentials
- Header with title and connection status
- Total Energy Generated banner (mint green)
- 4 Live metric cards with sparklines:
  - ⚡ Voltage (V)
  - 🔋 Energy (mJ)
  - 👟 No. of Presses (count)
  - 🔥 Power (mW)

## How to Connect Your Raspberry Pi

### Step 1: Start the Dashboard
The server is already running at: **http://localhost:8000**

### Step 2: Access Connection Settings
Click the **⚙️ Settings** button in the top right of the header

### Step 3: Configure Connection
1. Click **🔄** to refresh available serial ports
2. Select your Bluetooth COM port from the dropdown
3. Choose baud rate (default: 9600)
4. Click **Connect**

### Step 4: Monitor Data
- Data will appear instantly in the metric cards
- Sparklines show recent trends (last 30 points)
- Total energy accumulates automatically
- All cards update in real-time via WebSocket

## Hidden Features (Available via Settings)

### Real-time Voltage Graph
- Full 60-second timeline graph
- Access via Settings → Additional options

### Data Logging
- Start/Stop CSV logging
- Timestamped data saved to `/data` folder
- File format: `piezo_data_YYYYMMDD_HHMMSS.csv`

### LED Status
- Shows ON/OFF state from Raspberry Pi
- Hidden by default, can be shown via settings

## Data Format from Raspberry Pi

Your Raspberry Pi should send data like this:
```
Voltage: 2.84
Energy: 0.000404
Steps: 12
Power: 0.00007
LED: ON

------------------------------
```

## Troubleshooting

### "No ports found"
- Ensure Raspberry Pi is paired via Bluetooth
- Check Windows Bluetooth settings → More options → COM Ports
- Note the outgoing COM port number

### "Connection failed"
- Verify correct COM port selected
- Check baud rate matches Raspberry Pi (usually 9600)
- Try disconnecting and reconnecting Bluetooth

### "No data appearing"
- Check Raspberry Pi is sending data
- Verify data format matches expected format
- Look at browser console for errors (F12)

## Tech Stack
- **Backend**: Python with websockets
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js with sparkline support
- **Communication**: WebSocket for real-time updates
- **Serial**: PySerial for Bluetooth/COM port handling

## Files Location
```
piezo-dashboard/
├── backend/
│   ├── simple_server.py     # Main server (RUNNING)
│   └── simulate_data.py     # Test data generator
├── frontend/
│   ├── index.html          # Dashboard UI
│   ├── styles.css          # Clean light theme
│   └── app.js              # Real-time updates
└── data/                   # CSV logs saved here
```

## Quick Commands

### Restart Server
```bash
cd "d:\Github models\Pizeo-electric-electricity-generator\piezo-dashboard\backend"
python simple_server.py
```

### Test with Simulated Data
```bash
python backend/simulate_data.py COM3
```

## Next Steps
1. **Pair your Raspberry Pi** via Bluetooth
2. **Note the COM port** from Bluetooth settings
3. **Open the dashboard** (already at http://localhost:8000)
4. **Click Settings** → Select port → Connect
5. **Watch the data flow!** ⚡

---

**Your dashboard is production-ready and matches your design perfectly!** 🎉

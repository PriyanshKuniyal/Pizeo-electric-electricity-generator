# 🔌 Complete Setup Guide - Piezoelectric Dashboard

## ✅ What's Already Integrated

Your dashboard is **fully integrated** and ready to receive real-time data from your Arduino/Raspberry Pi! Here's what's working:

### Backend (Python Server)
- ✅ WebSocket server for real-time communication
- ✅ HTTP server for dashboard files
- ✅ Serial/Bluetooth connection handler
- ✅ Automatic data parsing from Arduino
- ✅ CSV logging system
- ✅ Dummy data generator (for testing)

### Frontend (Dashboard)
- ✅ Real-time data display with sparklines
- ✅ WebSocket connection (auto-reconnect)
- ✅ Total energy accumulation
- ✅ Settings panel for COM port selection
- ✅ Beautiful light theme matching your design

---

## 🚀 How to Use with Real Arduino Data

### Step 1: Arduino Code Format

Your Arduino **MUST** send data over Serial/Bluetooth in this **exact format**:

```
Voltage: 3.45
Energy: 0.000234
Steps: 152
Power: 0.00345
LED: ON
```

**Important Rules:**
- Each line must have `Key: Value` format
- Keys are case-insensitive: `voltage`, `Voltage`, or `VOLTAGE` all work
- Send all 5 values every time
- Separate multiple readings with a blank line or dashes `-------`
- Use newline `\n` after each line

### Step 2: Example Arduino Code

```cpp
void loop() {
  // Read your piezoelectric sensor
  float voltage = analogRead(A0) * (5.0 / 1023.0);
  float energy = calculateEnergy(); // Your calculation
  int steps = stepCounter;
  float power = voltage * voltage / resistance;
  
  // Send data in the required format
  Serial.println("Voltage: " + String(voltage, 2));
  Serial.println("Energy: " + String(energy, 6));
  Serial.println("Steps: " + String(steps));
  Serial.println("Power: " + String(power, 5));
  Serial.println("LED: " + String(ledState ? "ON" : "OFF"));
  Serial.println("-------"); // Separator (optional)
  
  delay(500); // Send data every 500ms
}
```

### Step 3: Connect Arduino/Raspberry Pi

#### Option A: USB Connection
1. Connect Arduino to your computer via USB
2. Note the COM port (e.g., COM3, COM4, or /dev/ttyUSB0 on Linux)

#### Option B: Bluetooth Connection
1. Pair your Bluetooth module (HC-05, HC-06, etc.) with your computer
2. Find the COM port assigned to the Bluetooth connection
   - Windows: Device Manager → Ports (COM & LPT)
   - Linux: `ls /dev/tty*`

### Step 4: Start the Dashboard

1. **Delete the dummy data file** (if you want real data):
   ```bash
   cd "d:\Github models\Pizeo-electric-electricity-generator\piezo-dashboard\backend"
   rm dummy_data.cfg
   ```

2. **Start the server** (if not already running):
   ```bash
   python simple_server.py
   ```

3. **Open the dashboard** in your browser:
   ```
   http://localhost:8888
   ```

### Step 5: Connect to Your Device

1. Click the **⚙️ SETTINGS** button in the top-right
2. Select your COM port from the dropdown
3. Set baud rate (default: 9600)
4. Click **Connect**
5. You should see **"Connected"** status turn green!

---

## 🎭 Testing with Dummy Data

If you want to test the dashboard **before** connecting real hardware:

1. **Create the dummy data file**:
   ```bash
   cd "d:\Github models\Pizeo-electric-electricity-generator\piezo-dashboard\backend"
   echo "enabled=true" > dummy_data.cfg
   ```

2. **Restart the server** - it will generate realistic dummy data every 0.5 seconds

3. **To stop dummy data**: Just delete `dummy_data.cfg` and the server will automatically switch to waiting for real sensor data

---

## 📊 Features You Can Use

### Real-time Monitoring
- **Voltage** (V) - with yellow sparkline
- **Energy** (mJ) - with blue sparkline  
- **No. of Presses** (count) - with cyan sparkline
- **Power** (mW) - with orange sparkline
- **Total Energy Generated** - accumulating banner at top

### Data Logging
1. Click **Start Logging** in the settings panel
2. Data will be saved to `data/piezo_data_YYYYMMDD_HHMMSS.csv`
3. Click **Stop Logging** when done
4. Open CSV file in Excel or any spreadsheet software

### Settings Panel
- **COM Port Selection** - auto-detects available ports
- **Baud Rate** - adjust to match your Arduino (9600, 115200, etc.)
- **Connect/Disconnect** - manage serial connection
- **Start/Stop Logging** - control CSV data recording

---

## 🔧 Troubleshooting

### "No data showing up"
✅ **Check Arduino is sending correct format** - Use Arduino Serial Monitor to verify output
✅ **Check COM port** - Make sure you selected the right port
✅ **Check baud rate** - Must match your Arduino code (default: 9600)
✅ **Check USB cable** - Some cables are power-only (no data)

### "Port already in use"
✅ **Close Arduino IDE Serial Monitor** - Can't have multiple connections
✅ **Restart the Python server** - Closes any stuck connections
✅ **Check Task Manager** - Kill any Python processes using the port

### "WebSocket disconnected"
✅ **Server still running?** - Check terminal for errors
✅ **Firewall blocking?** - Allow connections on ports 8888 and 8889
✅ **Page will auto-reconnect** - Wait 3 seconds, should reconnect automatically

### "Permission denied on COM port"
✅ **Windows**: Run VS Code as Administrator
✅ **Linux**: Add user to dialout group: `sudo usermod -a -G dialout $USER`

---

## 📁 File Structure

```
piezo-dashboard/
├── backend/
│   ├── simple_server.py       # Main server (WebSocket + HTTP + Serial)
│   ├── dummy_data.cfg         # Create this to enable dummy data
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html            # Dashboard UI
│   ├── styles.css            # Light theme styling
│   └── app.js                # WebSocket client + charts
└── data/
    └── piezo_data_*.csv      # Logged data files
```

---

## 🎯 Quick Start Checklist

- [ ] Python server running (`python simple_server.py`)
- [ ] Arduino code sending data in correct format
- [ ] Arduino connected via USB or Bluetooth
- [ ] Dashboard open in browser (`http://localhost:8888`)
- [ ] COM port selected in settings
- [ ] Click "Connect" button
- [ ] See green "Connected" status
- [ ] Data flowing to metrics and sparklines! 🎉

---

## 💡 Tips

1. **Test with dummy data first** - Make sure dashboard works before connecting hardware
2. **Use Serial Monitor** - Verify Arduino is sending correct format before connecting to dashboard
3. **Start with 9600 baud** - Most reliable, can increase later for faster updates
4. **Send data every 500ms** - Good balance between responsiveness and performance
5. **Keep browser tab active** - Some browsers throttle inactive tabs

---

## 🆘 Need Help?

If you encounter any issues:
1. Check the **browser console** (F12) for JavaScript errors
2. Check the **Python terminal** for server errors
3. Check the **Arduino Serial Monitor** to verify data format
4. Make sure all ports (8888, 8889) are not blocked by firewall

---

**Your dashboard is ready! Just connect your Arduino and watch the data flow! 🚀**

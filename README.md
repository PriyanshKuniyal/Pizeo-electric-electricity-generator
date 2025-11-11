# ⚡ Piezoelectric Energy Harvesting Dashboard

A complete IoT system for monitoring piezoelectric energy harvesting in real-time using Raspberry Pi Pico, HC-05 Bluetooth module, and a web-based dashboard.

---

## 🚀 Quick Start Guide

### 📋 Prerequisites

- **Python 3.8+** installed on your PC
- **Raspberry Pi Pico H** with MicroPython
- **HC-05 Bluetooth Module**
- **Piezoelectric voltage sensor**

---

## ⚡ Running the Dashboard

### For macOS (Automatic HC-05 Connection)

**Simply run:**

```bash
./start_dashboard_mac.sh
```

The dashboard will:
- ✅ Install dependencies automatically
- ✅ Auto-detect and connect to HC-05 Bluetooth
- ✅ Open at http://127.0.0.1:8000
- ✅ Start showing data immediately!

**First time setup:**
```bash
chmod +x start_dashboard_mac.sh
./start_dashboard_mac.sh
```

### For Windows

**Option 1: Double-click**
```
start_dashboard.bat
```

**Option 2: Command line**
```bash
cd piezo-dashboard && python backend/main.py
```

### Manual Installation

If you prefer to install step-by-step:

```bash
cd piezo-dashboard
pip install -r requirements.txt
cd backend
python main.py
```

The dashboard will open automatically at: **http://127.0.0.1:8000**

---

## 🔌 Hardware Setup

### Wiring Connections

| Component | Pico Pin | HC-05 Pin |
|-----------|----------|-----------|
| **Voltage Sensor** | GP27 (ADC1) | - |
| **HC-05 TX** | GP5 (RX) | TX |
| **HC-05 RX** | GP4 (TX) | RX |
| **HC-05 Power** | 3.3V | VCC |
| **HC-05 Ground** | GND | GND |

### Firmware Deployment

The firmware is already deployed on your Pico as `main.py`. It automatically runs on power-up.

If you need to redeploy:

```bash
mpremote connect COM11 cp firmware/voltage.py :main.py
mpremote connect COM11 reset
```

*(Replace COM11 with your Pico's COM port)*

---

## 📊 Connecting to Dashboard

1. **Open Dashboard**: http://127.0.0.1:8000
2. **Click "Refresh Ports"** button
3. **Select COM Port** from dropdown:
   - **For Bluetooth**: Select "Standard Serial over Bluetooth link (COMx)"
   - **For USB Direct**: Select your Pico's USB COM port
4. **Set Baud Rate**:
   - **9600** for Bluetooth (HC-05)
   - **115200** for USB direct connection
5. **Click "Connect"**
6. **Watch live data stream!** 📈

---

## 🎯 Features

### Real-Time Monitoring
- ✅ Live voltage measurements (0-16.3V)
- ✅ Instantaneous power calculation (P = V²/R)
- ✅ Energy accumulation tracking
- ✅ Interactive graphs and charts
- ✅ Statistical analysis

### Data Management
- ✅ CSV export functionality
- ✅ Historical data logging
- ✅ Real-time WebSocket streaming

### Connectivity
- ✅ **Bluetooth wireless** (HC-05)
- ✅ **USB serial** connection
- ✅ Auto-port detection

---

## 📂 Project Structure

```
Pizeo-electric-electricity-generator/
│
├── firmware/
│   ├── voltage.py              # Main firmware (deployed as main.py)
│   ├── bt_echo_test.py         # Bluetooth test utility
│   └── test.py                 # Voltage sensor test
│
├── piezo-dashboard/
│   ├── backend/
│   │   ├── main.py             # FastAPI server (RUN THIS!)
│   │   ├── simulate_data.py    # Demo mode
│   │   └── dummy_data.cfg      # Test data
│   │
│   ├── frontend/
│   │   ├── index.html          # Dashboard UI
│   │   ├── app.js              # Dashboard logic
│   │   └── styles.css          # Styling
│   │
│   ├── requirements.txt        # Python dependencies
│   ├── start_dashboard.bat     # Windows quick launcher
│   └── start_dashboard.sh      # Linux/Mac launcher
│
├── README.md                   # This file
└── LICENSE
```

---

## 🔧 Configuration

### Firmware Settings (firmware/voltage.py)

```python
# IMPORTANT: Use your TOTAL circuit resistance for accurate power calculations
LOAD_RESISTANCE = 1000.0  # Ohms - MUST measure your actual total resistance!
INTERVAL_S = 0.5          # Sampling interval (seconds)
USE_BLUETOOTH = True      # Enable/disable Bluetooth
```

### 📐 Measuring Total Circuit Resistance

For accurate power (P = V²/R) and energy calculations, you need the **total resistance**:

**Total Resistance = R_piezo + R_load + R_series + R_wiring**

#### Method 1: Direct Multimeter Measurement (Easiest)
1. Disconnect circuit from power
2. Set multimeter to Ω (resistance) mode
3. Measure across the entire circuit
4. This gives you **R_total** directly
5. Update `LOAD_RESISTANCE` in voltage.py

#### Method 2: Calculate from V and I
1. Connect circuit and let piezo generate voltage
2. Measure voltage (V) using your sensor
3. Measure current (I) using ammeter in series
4. Calculate: **R_total = V / I**
5. Update `LOAD_RESISTANCE` in voltage.py

#### Method 3: Sum Individual Resistances
```
R_total = R_piezo + R_load + R_protection + R_wiring

Example:
  R_piezo = 100Ω (internal resistance)
  R_load = 1000Ω (your load)
  R_protection = 50Ω (series resistor)
  R_wiring ≈ 5Ω (wire resistance)
  ─────────────────────────
  R_total = 1155Ω  ← Use this value!
```

**After measuring, update the firmware:**
```bash
# Edit voltage.py line 33
LOAD_RESISTANCE = 1155.0  # Your measured value

# Redeploy to Pico
mpremote connect COM11 cp firmware/voltage.py :main.py
mpremote connect COM11 reset
```

---

## 🔋 Understanding Power Calculations

The firmware calculates:

### Data Format

The Pico transmits data in this format:
```
V: 0.003V | P: 0.00mW | E_inst: 0.000mJ | E_total: 0.000mWh
```

---

## 🐛 Troubleshooting

### Dashboard Won't Start
```bash
# Reinstall dependencies
cd piezo-dashboard
pip install --upgrade fastapi uvicorn pydantic pyserial websockets
```

### No COM Ports Showing
- ✅ Check USB cable connection
- ✅ Verify Pico is powered (LED should be on)
- ✅ Install USB drivers if needed
- ✅ Try different USB port

### Bluetooth Not Working on PC
- ⚠️ Modern Windows 11 with Intel AX101/AX211 may lack SPP support
- ✅ **Solution 1**: Use USB connection instead (always works)
- ✅ **Solution 2**: Get USB Bluetooth adapter with SPP support
- ✅ **Solution 3**: Use different PC/laptop
- ✅ **Mac Users**: macOS has excellent Bluetooth SPP support - HC-05 works perfectly! Just run `./start_dashboard_mac.sh` and it will auto-connect!

### macOS: HC-05 Not Auto-Connecting
1. **Pair HC-05 first:**
   - Go to System Preferences → Bluetooth
   - Pair with "HC-05" (PIN: 1234 or 0000)
2. **Check port name:**
   ```bash
   ls /dev/tty.* | grep -i serial
   ```
   You should see something like `/dev/tty.HC-05-SerialPort`
3. **Run dashboard:**
   ```bash
   ./start_dashboard_mac.sh
   ```
   The dashboard will automatically detect and connect!

### No Data Appearing
- ✅ Verify correct COM port selected
- ✅ Check baud rate (9600 for BT, 115200 for USB)
- ✅ Click "Refresh Ports" and try again
- ✅ Restart Pico (unplug/replug power)

### Dashboard Shows Error
```bash
# Check if port is already in use
# Close other terminal programs (Arduino IDE, PuTTY, etc.)
# Restart dashboard server
```

---

## 📱 Mobile Monitoring

You can also monitor data directly on your phone:

1. Install **Bluetooth Serial Terminal** app (Android)
2. Pair with HC-05 (PIN: 1234)
3. Connect to HC-05
4. View live voltage data! 📊

---

## 🎓 Technical Specifications

### Hardware
- **MCU**: Raspberry Pi Pico (RP2040)
- **Bluetooth**: HC-05 Classic Bluetooth 2.0 (SPP)
- **ADC**: 12-bit, 0-3.3V input
- **Voltage Range**: 0-16.3V (with voltage divider)

### Software Stack
- **Backend**: FastAPI + Uvicorn
- **Frontend**: HTML5 + JavaScript + Chart.js
- **Communication**: WebSocket + Serial
- **Firmware**: MicroPython

### Performance
- **Sampling Rate**: 2 Hz (0.5s interval)
- **ADC Resolution**: 16-bit oversampled
- **Data Rate**: ~40 bytes/reading
- **Latency**: <100ms

---

## 🏆 Competition Ready

This project is **100% complete** and ready for demonstration:

✅ **Live monitoring** - Real-time voltage/power/energy display  
✅ **Wireless operation** - HC-05 Bluetooth transmission  
✅ **Data visualization** - Interactive graphs and charts  
✅ **Data logging** - CSV export and historical tracking  
✅ **Professional UI** - Modern, responsive dashboard  
✅ **Portable** - Works on any PC with Python  

---

## 📝 Quick Commands Reference

### Start Dashboard
```bash
cd piezo-dashboard && python backend/main.py
```

### Install Dependencies
```bash
cd piezo-dashboard && pip install -r requirements.txt
```

### Deploy Firmware to Pico
```bash
mpremote connect COM11 cp firmware/voltage.py :main.py
mpremote connect COM11 reset
```

### Test Bluetooth Connection
```bash
mpremote connect COM11 run firmware/bt_echo_test.py
```

### Check Available COM Ports
```bash
python -m serial.tools.list_ports
```

---

## 🌐 API Endpoints

The dashboard server provides these REST APIs:

- `GET /` - Dashboard web interface
- `GET /api/status` - Connection status
- `GET /api/ports` - Available serial ports
- `POST /api/connect` - Connect to device
- `POST /api/disconnect` - Disconnect device
- `WS /ws` - WebSocket for real-time data

---

## 📊 Data Export

To export collected data:

1. Click **"Start CSV Logging"** in dashboard
2. Data is saved to `piezo-dashboard/data/sensor_data_YYYYMMDD_HHMMSS.csv`
3. Format: `timestamp, voltage, energy, steps, power, led`

---

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

## 📄 License

See LICENSE file for details.

---

## 👨‍💻 Author

**Priyansh Kuniyal**

---

## 🎉 Quick Start Summary

**Just want to run it? Copy-paste these commands:**

### For Windows:
```bash
# 1. Install dependencies (first time only)
cd piezo-dashboard
pip install -r requirements.txt

# 2. Start dashboard server
python backend/main.py

# 3. Open browser: http://127.0.0.1:8000
# 4. In dashboard:
#    - Click "Refresh Ports"
#    - Select your COM port (e.g., COM4, COM11)
#    - Set baud rate (9600 for BT, 115200 for USB)
#    - Click "Connect"
#    - Enjoy live data! 🎉
```

### For macOS (Mac M1/M2):
```bash
# 1. Install dependencies (first time only)
cd piezo-dashboard
pip3 install -r requirements.txt

# 2. Pair HC-05 Bluetooth
# System Preferences → Bluetooth → Add HC-05 (PIN: 1234)

# 3. Start dashboard server
python3 backend/main.py

# 4. Open browser: http://127.0.0.1:8000
# 5. In dashboard:
#    - Click "Refresh Ports"
#    - Select your port (e.g., /dev/tty.HC-05-DevB or /dev/tty.usbmodem*)
#    - Set baud rate (9600 for BT, 115200 for USB)
#    - Click "Connect"
#    - Enjoy live data! 🎉
```

**Note:** macOS has excellent Bluetooth SPP support - HC-05 works perfectly without any issues!

---

**Made with ⚡ by Priyansh Kuniyal**

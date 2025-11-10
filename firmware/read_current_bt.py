"""PC-side helper to read current sensor data from HC-05 Bluetooth serial.
Auto-detects HC-05 COM port and prints incoming current readings.
Requires: pip install pyserial
Run: python read_current_bt.py
Press Ctrl+C to exit.
"""
import sys
import time
import serial
import serial.tools.list_ports

TARGET_NAMES = ("HC", "HC-05", "Bluetooth")
BAUD = 9600

def find_port():
    """Auto-detect HC-05 Bluetooth COM port."""
    for p in serial.tools.list_ports.comports():
        desc = (p.description or "") + " " + (p.name or "")
        if any(name.lower() in desc.lower() for name in TARGET_NAMES):
            return p.device
    return None

def main():
    port = find_port()
    if not port:
        print("HC-05 port not found. Pair the module first. Current ports:")
        for p in serial.tools.list_ports.comports():
            print(" -", p.device, p.description)
        sys.exit(1)
    
    print(f"Connecting to {port} at {BAUD} baud ...")
    try:
        ser = serial.Serial(port, BAUD, timeout=2)
    except Exception as e:
        print("Failed to open port:", e)
        sys.exit(1)
    
    print("Reading current data. Ctrl+C to quit.\n")
    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if line:
                print(line)
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        print("\nClosed.")

if __name__ == "__main__":
    main()

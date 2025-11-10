"""
Force connect to HC-05 Bluetooth COM port
Works even when Windows shows HC-05 as 'not connected'
"""
import serial
import time

# Try all common HC-05 Bluetooth COM ports
BT_PORTS = ["COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10", "COM13", "COM14"]
BAUD = 9600

print("HC-05 Force Connect Utility")
print("=" * 60)
print("This will try to open HC-05 COM port directly")
print("=" * 60)

for port in BT_PORTS:
    print(f"\nTrying {port}...", end=" ", flush=True)
    try:
        # Try to open with extended timeout and force DTR/RTS
        ser = serial.Serial(
            port=port,
            baudrate=BAUD,
            timeout=1,
            write_timeout=1,
            dsrdtr=True,
            rtscts=False
        )
        
        # Sometimes need to wake up the port
        ser.dtr = True
        ser.rts = False
        time.sleep(0.1)
        
        print("OPENED!")
        print(f"Listening on {port} for data from Pico...")
        print("-" * 60)
        
        # Read data
        no_data_count = 0
        try:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        print(line)
                        no_data_count = 0
                else:
                    time.sleep(0.1)
                    no_data_count += 1
                    if no_data_count > 50:  # 5 seconds no data
                        print(f"No data for 5 seconds on {port}, trying next port...")
                        break
        except KeyboardInterrupt:
            print("\n\nStopped by user.")
            ser.close()
            exit(0)
        
        ser.close()
        
    except serial.SerialException as e:
        if "PermissionError" in str(e) or "Access is denied" in str(e):
            print("BUSY (another program using it)")
        elif "FileNotFoundError" in str(e):
            print("doesn't exist")
        else:
            print(f"Error: {str(e)[:40]}")
    except Exception as e:
        print(f"Error: {str(e)[:40]}")

print("\n" + "=" * 60)
print("No active HC-05 data found on any port.")
print("=" * 60)
print("\nTroubleshooting:")
print("1. Make sure Pico is powered and running (COM11 connected)")
print("2. Check HC-05 LED: slow blink = ready, fast blink = not paired")
print("3. Verify wiring: Pico GP0 → HC-05 RX, GP1 → HC-05 TX")
print("4. Try removing and re-pairing HC-05 in Windows Settings")

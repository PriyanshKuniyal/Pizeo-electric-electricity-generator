"""
Force open HC-05 paired COM port and trigger active connection
This forces Windows to activate the Bluetooth SPP connection
"""
import serial
import time
import serial.tools.list_ports

print("HC-05 Connection Forcer")
print("=" * 60)
print("This will attempt to force-activate the Bluetooth connection")
print("=" * 60)

# Find all Bluetooth COM ports
bt_ports = []
for p in serial.tools.list_ports.comports():
    if "Bluetooth" in (p.description or ""):
        bt_ports.append(p.device)
        print(f"Found Bluetooth port: {p.device}")

if not bt_ports:
    print("\nNo Bluetooth COM ports found!")
    print("Make sure HC-05 is paired (Settings → Bluetooth → HC-05 should show as Paired)")
    exit(1)

print(f"\nTrying to force connection on {len(bt_ports)} ports...")
print("-" * 60)

for port in bt_ports:
    print(f"\n[{port}] Attempting connection...", end=" ", flush=True)
    
    for attempt in range(3):  # Try 3 times per port
        try:
            # Try to open with aggressive settings
            ser = serial.Serial(
                port=port,
                baudrate=9600,
                timeout=0.5,
                write_timeout=0.5,
                dsrdtr=True,
                rtscts=False,
                xonxoff=False
            )
            
            # Force DTR/RTS
            ser.dtr = True
            ser.rts = False
            time.sleep(0.2)
            
            # Try to wake it up by sending data
            ser.write(b"\r\n")
            time.sleep(0.1)
            
            print(f"OPENED (attempt {attempt+1})!")
            print(f"[{port}] Waiting for data from Pico...")
            
            # Listen for 10 seconds
            start = time.time()
            data_received = False
            
            while time.time() - start < 10:
                if ser.in_waiting > 0:
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        if not data_received:
                            print(f"\n{'='*60}")
                            print(f"SUCCESS! DATA RECEIVED ON {port}")
                            print(f"{'='*60}\n")
                            data_received = True
                        print(line)
                time.sleep(0.05)
            
            if data_received:
                print(f"\n{'='*60}")
                print("Connection successful! Press Ctrl+C to stop.")
                print(f"{'='*60}\n")
                try:
                    while True:
                        if ser.in_waiting > 0:
                            line = ser.readline().decode(errors='ignore').strip()
                            if line:
                                print(line)
                        time.sleep(0.05)
                except KeyboardInterrupt:
                    pass
                ser.close()
                exit(0)
            else:
                print(f" no data in 10s")
                ser.close()
                break
                
        except serial.SerialException as e:
            if "Access is denied" in str(e) or "PermissionError" in str(e):
                print(f" BUSY")
                break
            elif attempt == 2:
                print(f" FAILED after 3 attempts: {str(e)[:30]}")
        except Exception as e:
            if attempt == 2:
                print(f" ERROR: {str(e)[:30]}")
        
        time.sleep(0.3)

print("\n" + "=" * 60)
print("DIAGNOSIS:")
print("=" * 60)
print("✗ No data received on any Bluetooth COM port")
print("\nPossible causes:")
print("1. HC-05 is paired but Windows hasn't activated the SPP connection")
print("2. Pico not sending data (verify with: mpremote connect COM11 run firmware/uart_test.py)")
print("3. HC-05 wiring issue (GP0→RX, 3.3V→VCC, GND→GND)")
print("\nWorkaround: Use USB connection - it's working perfectly!")
print("Command: mpremote connect COM11 run firmware/voltage.py")

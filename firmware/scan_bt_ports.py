"""Try all Bluetooth COM ports to find active HC-05 connection"""
import serial
import serial.tools.list_ports
import time

print("Scanning all Bluetooth COM ports for HC-05 data...")
print("-" * 60)

bt_ports = []
for p in serial.tools.list_ports.comports():
    if "Bluetooth" in (p.description or ""):
        bt_ports.append(p.device)

if not bt_ports:
    print("No Bluetooth COM ports found. Please pair HC-05 first.")
    exit(1)

print(f"Found {len(bt_ports)} Bluetooth ports: {', '.join(bt_ports)}")
print("Trying each port...\n")

for port in bt_ports:
    print(f"Trying {port}...", end=" ")
    try:
        ser = serial.Serial(port, 9600, timeout=2)
        print("OPENED - listening for data...")
        
        # Try to read for 3 seconds
        start = time.time()
        got_data = False
        while time.time() - start < 3:
            if ser.in_waiting:
                line = ser.readline().decode(errors='ignore').strip()
                if line:
                    print(f"  ✓ GOT DATA: {line}")
                    got_data = True
                    break
        
        if not got_data:
            print("  ✗ No data received (might not be connected)")
        else:
            print(f"\n{'='*60}")
            print(f"SUCCESS! HC-05 is on {port}")
            print(f"{'='*60}")
            print("Reading continuous data... Press Ctrl+C to stop\n")
            
            try:
                while True:
                    line = ser.readline().decode(errors='ignore').strip()
                    if line:
                        print(line)
            except KeyboardInterrupt:
                pass
            
            ser.close()
            break
        
        ser.close()
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:50]}")

print("\nScan complete.")

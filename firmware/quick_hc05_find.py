"""
Quick HC-05 Data Finder
Since HC-05 is not connected to phone, let's find which COM port has data
"""
import serial
import time

print("=" * 70)
print("SEARCHING FOR HC-05 DATA ON PC BLUETOOTH PORTS")
print("=" * 70)
print()
print("Make sure:")
print("  ✓ Pico is powered on")
print("  ✓ HC-05 is disconnected from phone app")
print("  ✓ HC-05 LED is blinking (searching for connection)")
print()

# These ports opened successfully in the previous test
working_ports = ['COM4', 'COM6', 'COM7', 'COM10', 'COM13', 'COM14']

print(f"Testing {len(working_ports)} available Bluetooth ports...")
print("This will take about 30 seconds...")
print()

for port_name in working_ports:
    print(f"[{port_name}] Opening...", end=" ", flush=True)
    
    try:
        # Open the port
        ser = serial.Serial(port_name, 9600, timeout=1)
        print("Connected.", end=" ", flush=True)
        
        # Wait a moment for data
        time.sleep(0.5)
        
        # Try to read for 5 seconds
        print("Listening...", end=" ", flush=True)
        found_data = False
        start_time = time.time()
        
        while time.time() - start_time < 5:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                
                # Check if it's our HC-05 data format
                if 'V:' in data or 'P:' in data or 'E_total' in data:
                    print("\n")
                    print("  " + "=" * 66)
                    print(f"  ✅ FOUND HC-05 DATA ON {port_name}!")
                    print("  " + "=" * 66)
                    print()
                    print("  Data received:")
                    print("  " + "-" * 66)
                    for line in data.strip().split('\n')[:5]:
                        if line.strip():
                            print(f"  {line}")
                    print("  " + "-" * 66)
                    print()
                    print(f"  ✅ USE THIS PORT IN DASHBOARD: {port_name}")
                    print(f"  ✅ BAUD RATE: 9600")
                    print()
                    found_data = True
                    ser.close()
                    break
            
            time.sleep(0.1)
        
        if not found_data:
            print("No HC-05 data")
        
        ser.close()
        
        if found_data:
            break
            
    except serial.SerialException as e:
        if "timeout" in str(e).lower() or "semaphore" in str(e).lower():
            print("Timeout (no device)")
        else:
            print(f"Error: {str(e)[:40]}")
    except Exception as e:
        print(f"Error: {str(e)[:40]}")

print()
print("=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print()
print("If HC-05 data was found:")
print("  1. Note the COM port number")
print("  2. Open dashboard: http://127.0.0.1:8000")
print("  3. Click 'Connect' or 'Settings'")
print("  4. Select the COM port shown above")
print("  5. Set baud rate: 9600")
print("  6. Click 'Connect'")
print()
print("If NO data was found:")
print("  • HC-05 might need to be 'activated' to transmit to PC")
print("  • Try connecting once from phone app, then disconnect")
print("  • Or the HC-05 might only work with phone pairing")
print()
print("ALTERNATIVE:")
print("  • Continue using phone app to monitor voltage")
print("  • Dashboard can run in demo mode for testing UI")
print("=" * 70)

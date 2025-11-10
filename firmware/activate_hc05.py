"""
Force HC-05 Connection by Sending Data
This will attempt to "wake up" the HC-05 connection by writing to each port
"""
import serial
import time

print("=" * 70)
print("HC-05 CONNECTION ACTIVATOR")
print("=" * 70)
print()

print("This script will try to ACTIVATE the HC-05 connection")
print("by sending data to each Bluetooth COM port.")
print()

# Available ports
ports_to_try = ['COM4', 'COM6', 'COM7', 'COM10', 'COM13', 'COM14']

print(f"Testing {len(ports_to_try)} Bluetooth ports...")
print()

print("IMPORTANT: Make sure:")
print("  ✓ Pico is powered ON (red LED lit)")
print("  ✓ HC-05 is NOT connected to your phone")
print("  ✓ HC-05 LED is blinking")
print()

input("Press ENTER to start testing...")
print()

for port_name in ports_to_try:
    print(f"\n{'=' * 70}")
    print(f"Testing {port_name}")
    print('=' * 70)
    
    try:
        # Try to open the port with specific settings
        print(f"  → Opening {port_name} at 9600 baud...", end=" ", flush=True)
        
        ser = serial.Serial(
            port=port_name,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )
        
        print("✓ Opened")
        
        # Set DTR and RTS to activate the connection
        print(f"  → Activating DTR/RTS signals...", end=" ", flush=True)
        ser.setDTR(True)
        ser.setRTS(True)
        time.sleep(0.5)
        print("✓ Done")
        
        # Clear any existing data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Try to trigger a response by sending a newline
        print(f"  → Sending wake-up signal...", end=" ", flush=True)
        ser.write(b'\r\n')
        time.sleep(0.5)
        print("✓ Done")
        
        # Now listen for data
        print(f"  → Listening for HC-05 data (10 seconds)...")
        
        start_time = time.time()
        data_found = False
        
        while time.time() - start_time < 10:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                
                # Check for our data format
                if 'V:' in data or 'P:' in data or 'mW' in data:
                    print()
                    print("  " + "🎉" * 35)
                    print(f"  ✅✅✅ SUCCESS! HC-05 IS ACTIVE ON {port_name}! ✅✅✅")
                    print("  " + "🎉" * 35)
                    print()
                    print("  Data received:")
                    print("  " + "-" * 66)
                    for line in data.strip().split('\n')[:10]:
                        if line.strip():
                            print(f"  {line}")
                    print("  " + "-" * 66)
                    print()
                    print(f"  ✅ HC-05 COM PORT: {port_name}")
                    print(f"  ✅ BAUD RATE: 9600")
                    print()
                    print("  Now you can:")
                    print(f"    1. Use PuTTY with {port_name} at 9600 baud")
                    print(f"    2. Use dashboard with {port_name} at 9600 baud")
                    print()
                    data_found = True
                    break
            
            # Show we're still listening
            elapsed = int(time.time() - start_time)
            print(f"     Listening... {elapsed}/10 seconds", end='\r', flush=True)
            time.sleep(0.2)
        
        if not data_found:
            print()
            print(f"  ✗ No HC-05 data received on {port_name}")
        
        ser.close()
        
        if data_found:
            print()
            print("=" * 70)
            print("CONNECTION SUCCESSFUL!")
            print("=" * 70)
            print()
            print(f"Your HC-05 is working on {port_name}!")
            print()
            print("The connection should now stay active.")
            print("Try PuTTY or the dashboard with this port.")
            print()
            break
            
    except serial.SerialException as e:
        error_msg = str(e)
        if "PermissionError" in error_msg or "in use" in error_msg.lower():
            print(f"  ✗ Port is in use by another program")
        elif "timeout" in error_msg.lower() or "semaphore" in error_msg.lower():
            print(f"  ✗ Timeout - device not responding")
        elif "FileNotFoundError" in error_msg or "could not open" in error_msg.lower():
            print(f"  ✗ Port doesn't exist or can't be opened")
        else:
            print(f"  ✗ Error: {error_msg}")
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
    
    time.sleep(0.5)

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print()

print("If NO port showed data:")
print()
print("POSSIBLE CAUSES:")
print("  1. HC-05 is still connected to your phone")
print("     → Check phone Bluetooth settings")
print("     → Disconnect or unpair HC-05")
print()
print("  2. Pico is not powered or not running")
print("     → Check red LED on Pico is lit")
print("     → Try unplugging and replugging power")
print()
print("  3. HC-05 wiring issue")
print("     → Verify: GP4 → HC-05 RX")
print("     → Verify: GP5 → HC-05 TX")
print("     → Verify: 3.3V → HC-05 VCC")
print("     → Verify: GND → HC-05 GND")
print()
print("  4. Windows Bluetooth doesn't support SPP properly")
print("     → This is a Windows limitation")
print("     → Consider using USB Bluetooth adapter")
print("     → Or continue using your phone (which works!)")
print()
print("NEXT STEPS:")
print("  • Try unplugging Pico power for 5 seconds")
print("  • Plug it back in")
print("  • Wait for HC-05 LED to start blinking")
print("  • Run this script again")
print()
print("=" * 70)

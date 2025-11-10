"""
Step-by-step guide to connect HC-05 to PC and find the correct COM port
"""
import serial.tools.list_ports
import time

def check_bluetooth_ports():
    """Check all Bluetooth COM ports"""
    ports = serial.tools.list_ports.comports()
    bt_ports = []
    
    for port in ports:
        desc = port.description.lower()
        if 'bluetooth' in desc:
            bt_ports.append({
                'port': port.device,
                'desc': port.description,
                'hwid': port.hwid
            })
    
    return bt_ports

print("=" * 70)
print("HC-05 TO PC CONNECTION GUIDE")
print("=" * 70)
print()

print("STEP 1: Disconnect HC-05 from Phone")
print("-" * 70)
print("  • Open Bluetooth settings on your phone")
print("  • Find 'HC-05' or 'H-C-2010-06-01'")
print("  • Tap → Disconnect or Unpair")
print("  • HC-05 LED should start FAST blinking (searching for connection)")
print()
input("Press ENTER when you've disconnected from phone...")
print()

print("STEP 2: Pair HC-05 with Windows PC")
print("-" * 70)
print("  • Press Windows + I to open Settings")
print("  • Go to: Bluetooth & devices → Add device → Bluetooth")
print("  • Look for 'HC-05' or 'H-C-2010-06-01' in the list")
print("  • Click on it to pair")
print("  • If asked for PIN, try: 1234 or 0000")
print("  • Wait for 'Connected' message")
print("  • HC-05 LED should change to SLOW blinking (connected)")
print()
input("Press ENTER when HC-05 is paired and connected to PC...")
print()

print("STEP 3: Finding HC-05 COM Port")
print("-" * 70)
print("Scanning Bluetooth COM ports...")
print()

bt_ports = check_bluetooth_ports()

if not bt_ports:
    print("❌ No Bluetooth COM ports found!")
    print()
    print("TROUBLESHOOTING:")
    print("  1. Make sure HC-05 is paired in Windows Settings")
    print("  2. Check Device Manager → Ports (COM & LPT)")
    print("  3. Look for 'Standard Serial over Bluetooth link'")
    print()
    exit(1)

print(f"✅ Found {len(bt_ports)} Bluetooth COM port(s):")
print()

for i, port_info in enumerate(bt_ports, 1):
    print(f"  {i}. {port_info['port']} - {port_info['desc']}")

print()
print("-" * 70)
print("STEP 4: Test Each Port for HC-05 Data")
print("-" * 70)
print()

active_port = None

for port_info in bt_ports:
    port_name = port_info['port']
    print(f"Testing {port_name}...", end=" ", flush=True)
    
    try:
        ser = serial.Serial(port_name, 9600, timeout=2)
        time.sleep(1)
        
        # Try to read data for 3 seconds
        start = time.time()
        data_found = False
        
        while time.time() - start < 3:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                if 'V:' in data or 'P:' in data:
                    print("✅ FOUND HC-05 DATA!")
                    print(f"   Sample: {data[:80]}")
                    active_port = port_name
                    data_found = True
                    break
            time.sleep(0.1)
        
        if not data_found:
            print("No data")
        
        ser.close()
        
        if active_port:
            break
            
    except serial.SerialException as e:
        print(f"Cannot open (might be in use)")
    except Exception as e:
        print(f"Error: {e}")

print()
print("=" * 70)

if active_port:
    print(f"✅ SUCCESS! HC-05 is on: {active_port}")
    print()
    print("NEXT STEPS:")
    print(f"  1. Open your dashboard at http://127.0.0.1:8000")
    print(f"  2. Click 'Connect' or 'Settings'")
    print(f"  3. Select port: {active_port}")
    print(f"  4. Set baud rate: 9600")
    print(f"  5. Click 'Connect'")
    print()
    print("You should now see real-time voltage data on the dashboard!")
else:
    print("❌ No data found on any port")
    print()
    print("TROUBLESHOOTING:")
    print("  1. Check HC-05 LED - should be SLOW blinking (connected)")
    print("  2. Make sure Pico is powered on and running")
    print("  3. Verify wiring: GP4→HC-05 RX, GP5→HC-05 TX")
    print("  4. Try disconnecting and reconnecting HC-05 in Windows Settings")
    print("  5. Check Device Manager for the correct COM port")
    print()
    print("TO MANUALLY TEST A PORT:")
    print("  • Open dashboard")
    print("  • Try each Bluetooth COM port one by one")
    print("  • Look for voltage data appearing")

print("=" * 70)

"""
Find which COM port is receiving data from HC-05
This will test all Bluetooth COM ports and show which one has data
"""
import serial
import serial.tools.list_ports
import time

def find_bluetooth_ports():
    """Find all Bluetooth COM ports"""
    ports = serial.tools.list_ports.comports()
    bt_ports = []
    
    for port in ports:
        desc = port.description.lower()
        if 'bluetooth' in desc:
            bt_ports.append((port.device, port.description))
    
    return bt_ports

def test_port(port_name, timeout=3):
    """Test if a port is receiving data"""
    try:
        ser = serial.Serial(port_name, 9600, timeout=1)
        print(f"  Testing {port_name}...", end=" ")
        
        start_time = time.time()
        data_received = False
        
        while time.time() - start_time < timeout:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                if data.strip():
                    print(f"✓ FOUND DATA!")
                    print(f"  Sample: {data[:100]}")
                    data_received = True
                    break
            time.sleep(0.1)
        
        if not data_received:
            print("✗ No data")
        
        ser.close()
        return data_received
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("HC-05 Bluetooth Port Finder")
    print("=" * 60)
    print("\nMake sure:")
    print("  1. HC-05 is paired with your PC")
    print("  2. Pico is powered on and running main.py")
    print("  3. HC-05 LED is blinking slowly (connected)")
    print()
    
    bt_ports = find_bluetooth_ports()
    
    if not bt_ports:
        print("❌ No Bluetooth COM ports found!")
        print("   Make sure HC-05 is paired in Windows Bluetooth settings")
        exit(1)
    
    print(f"Found {len(bt_ports)} Bluetooth COM port(s):\n")
    
    for port, desc in bt_ports:
        print(f"📡 {port}: {desc}")
    
    print("\n" + "=" * 60)
    print("Testing ports for HC-05 data...")
    print("=" * 60 + "\n")
    
    active_port = None
    
    for port, desc in bt_ports:
        if test_port(port, timeout=3):
            active_port = port
            break
    
    print("\n" + "=" * 60)
    if active_port:
        print(f"✅ HC-05 is transmitting on: {active_port}")
        print(f"\nUse this port in the dashboard!")
    else:
        print("❌ No data found on any Bluetooth port")
        print("\nTroubleshooting:")
        print("  1. Check if HC-05 LED is slow blinking (connected)")
        print("  2. Make sure Pico is powered and running")
        print("  3. Verify wiring: GP4→HC-05 RX, GP5→HC-05 TX")
        print("  4. Try disconnecting/reconnecting HC-05 on your phone first")
    print("=" * 60)

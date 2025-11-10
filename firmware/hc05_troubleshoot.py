"""
HC-05 Windows Connection Troubleshooter
Diagnoses why HC-05 pairs but doesn't connect
"""
import subprocess
import serial.tools.list_ports

print("=" * 70)
print("HC-05 WINDOWS CONNECTION DIAGNOSTICS")
print("=" * 70)
print()

print("ISSUE: HC-05 pairs but doesn't connect to PC")
print("REASON: Windows may not have proper SPP (Serial Port Profile) drivers")
print()

# Check available Bluetooth ports
print("Step 1: Checking Bluetooth COM Ports")
print("-" * 70)
ports = serial.tools.list_ports.comports()
bt_ports = [p for p in ports if 'bluetooth' in p.description.lower()]

if bt_ports:
    print(f"✅ Found {len(bt_ports)} Bluetooth COM port(s):")
    for port in bt_ports:
        print(f"   {port.device}: {port.description}")
else:
    print("❌ No Bluetooth COM ports found!")
    print()
    print("This means Windows hasn't created a Serial Port Profile (SPP)")
    print("for the HC-05 connection.")

print()
print("=" * 70)
print("SOLUTION: Manual SPP Setup for HC-05")
print("=" * 70)
print()

print("METHOD 1: Add Outgoing COM Port (RECOMMENDED)")
print("-" * 70)
print("1. Press Windows + X → Device Manager")
print("2. Find 'Bluetooth' section → Expand it")
print("3. Look for 'HC-05' or 'H-C-2010-06-01'")
print("4. Right-click on it → Properties")
print("5. Go to 'Services' tab")
print("6. Check if 'Serial Port Profile (SPP)' is listed")
print("7. If not, we need to manually add COM port...")
print()

print("ALTERNATIVE: Add COM Port Manually")
print("-" * 70)
print("1. Open Device Manager")
print("2. Go to: Bluetooth → Your Bluetooth Adapter")
print("3. Right-click → Properties → COM Ports tab")
print("4. Click 'Add' → Select 'Outgoing'")
print("5. This creates a COM port for outgoing SPP connections")
print()

print("METHOD 2: Use PuTTY Instead")
print("-" * 70)
print("Sometimes 3rd party terminal software works better:")
print("1. Download PuTTY: https://putty.org")
print("2. Set Connection Type: Serial")
print("3. Try each Bluetooth COM port (COM3-COM14)")
print("4. Set Speed: 9600")
print("5. Click Open")
print()

print("METHOD 3: Check Device Manager for Hidden Devices")
print("-" * 70)
print("1. Open Device Manager")
print("2. Click View → Show Hidden Devices")
print("3. Look under 'Ports (COM & LPT)'")
print("4. Find 'Standard Serial over Bluetooth link'")
print("5. Note the COM port number (e.g., COM5)")
print("6. Try connecting to that specific port")
print()

print("=" * 70)
print("QUICK TEST: Try Opening Ports Directly")
print("=" * 70)
print()

if bt_ports:
    print("Let me try to open each Bluetooth port...")
    print()
    
    for port in bt_ports:
        port_name = port.device
        print(f"Testing {port_name}...", end=" ", flush=True)
        
        try:
            ser = serial.Serial(port_name, 9600, timeout=1)
            print(f"✅ Port opened successfully!")
            print(f"   → This port is available for use")
            ser.close()
        except serial.SerialException as e:
            if "PermissionError" in str(e) or "in use" in str(e).lower():
                print(f"⚠️  Port is in use (possibly by another program)")
            elif "timeout" in str(e).lower() or "semaphore" in str(e).lower():
                print(f"⚠️  Timeout - HC-05 may not be connected")
            else:
                print(f"❌ Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print()
    print("=" * 70)
    print("RECOMMENDATION:")
    print("=" * 70)
    print()
    print("If ports timeout or can't open, the HC-05 needs an active connection.")
    print()
    print("TRY THIS:")
    print("1. Keep HC-05 paired in Windows")
    print("2. Keep Pico powered on (sending data)")
    print("3. In Device Manager, find HC-05 device")
    print("4. Right-click → Connect (if option available)")
    print("5. HC-05 LED should go from fast blink to slow blink")
    print("6. Then try opening the COM port again")
    print()
    print("OR USE YOUR PHONE:")
    print("Since HC-05 works perfectly with your phone, you can:")
    print("1. Keep using phone to view real-time data")
    print("2. Use the dashboard in 'Demo Mode' to test features")
    print("3. Or get a USB Bluetooth adapter with better SPP support")
    
else:
    print()
    print("=" * 70)
    print("CRITICAL ISSUE: No Bluetooth COM Ports")
    print("=" * 70)
    print()
    print("Your Windows PC has paired with HC-05 but hasn't created")
    print("any Serial Port Profile (SPP) COM ports.")
    print()
    print("SOLUTIONS:")
    print()
    print("1. UPDATE BLUETOOTH DRIVERS:")
    print("   - Open Device Manager")
    print("   - Find your Bluetooth adapter")
    print("   - Right-click → Update Driver")
    print("   - Search automatically for drivers")
    print()
    print("2. INSTALL BLUETOOTH DRIVERS WITH SPP SUPPORT:")
    print("   - Some newer Windows 11 systems lack SPP support")
    print("   - You may need older Intel/Broadcom Bluetooth drivers")
    print()
    print("3. USE USB BLUETOOTH DONGLE:")
    print("   - Get a USB Bluetooth adapter with SPP support")
    print("   - Plugable USB-BT4LE or similar")
    print("   - These usually have better Classic Bluetooth support")
    print()
    print("4. CONTINUE USING YOUR PHONE:")
    print("   - HC-05 works perfectly with your phone")
    print("   - This is actually the most reliable solution")
    print("   - Phone Bluetooth apps have full SPP support")

print()
print("=" * 70)

"""
HC-05 Bluetooth Driver Checker and Fixer
Diagnose and fix Windows Bluetooth SPP driver issues
"""
import subprocess
import sys

print("=" * 70)
print("HC-05 BLUETOOTH DRIVER DIAGNOSTIC & FIX")
print("=" * 70)
print()

print("Step 1: Checking Current Bluetooth Adapter Information")
print("-" * 70)

try:
    # Get Bluetooth adapter info
    result = subprocess.run(
        ['powershell', '-Command', 
         'Get-PnpDevice -Class Bluetooth | Select-Object FriendlyName, Status, DriverVersion | Format-Table -AutoSize'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Could not retrieve Bluetooth adapter info")
        print()
except Exception as e:
    print(f"Error checking Bluetooth: {e}")
    print()

print()
print("Step 2: Checking for HC-05 Pairing Status")
print("-" * 70)

try:
    result = subprocess.run(
        ['powershell', '-Command',
         'Get-PnpDevice | Where-Object {$_.FriendlyName -like "*HC*" -or $_.FriendlyName -like "*H-C*"} | Format-Table FriendlyName, Status'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0 and result.stdout.strip():
        print(result.stdout)
    else:
        print("HC-05 not found in paired devices")
        print()
except Exception as e:
    print(f"Could not check HC-05 status")
    print()

print()
print("=" * 70)
print("DIAGNOSIS & SOLUTIONS")
print("=" * 70)
print()

print("ISSUE: HC-05 pairs but doesn't establish SPP (Serial Port) connection")
print()
print("ROOT CAUSE:")
print("  • Windows 10/11 prioritized BLE (Bluetooth Low Energy)")
print("  • Classic Bluetooth SPP support is incomplete in modern Windows")
print("  • HC-05 uses Classic Bluetooth 2.0 SPP protocol")
print("  • COM ports exist but no active data connection established")
print()

print("=" * 70)
print("SOLUTION 1: Manual COM Port Activation (TRY THIS FIRST)")
print("=" * 70)
print()
print("Force Windows to establish the SPP connection:")
print()
print("METHOD A: Device Manager")
print("-" * 70)
print("1. Press Windows + X → Device Manager")
print("2. Expand 'Bluetooth' section")
print("3. Find your Bluetooth adapter (e.g., 'Intel Wireless Bluetooth')")
print("4. Right-click → Properties")
print("5. Look for 'COM Ports' or 'Services' tab")
print("6. If you see 'Add', click it and add an 'Outgoing' port")
print("7. This should activate the SPP connection")
print()

print("METHOD B: Bluetooth Settings")
print("-" * 70)
print("1. Windows Settings → Bluetooth & devices")
print("2. Click 'More Bluetooth settings' or 'Devices and printers'")
print("3. Find HC-05 device")
print("4. Right-click → Properties")
print("5. Look for 'Services' tab")
print("6. Enable 'Serial Port' service if not checked")
print()

print("METHOD C: Re-pair with PIN")
print("-" * 70)
print("1. Remove/Forget HC-05 from Windows Bluetooth")
print("2. Power cycle the HC-05 (unplug and replug)")
print("3. Pair again")
print("4. When asked for PIN, enter: 1234")
print("5. This sometimes triggers proper SPP initialization")
print()

print("=" * 70)
print("SOLUTION 2: Install PuTTY (Quick Test)")
print("=" * 70)
print()
print("PuTTY can sometimes activate dormant COM ports:")
print()
print("1. Download: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html")
print("2. Install and open PuTTY")
print("3. Select 'Serial' connection type")
print("4. Try ports: COM4, COM6, COM7, COM10, COM13, COM14")
print("5. Set Speed: 9600")
print("6. Click 'Open'")
print("7. If it connects, you should see voltage data appear!")
print()

print("=" * 70)
print("SOLUTION 3: Update/Reinstall Bluetooth Drivers")
print("=" * 70)
print()
print("If your Bluetooth adapter lacks proper SPP support:")
print()
print("Option A: Update Current Driver")
print("-" * 70)
print("1. Device Manager → Bluetooth → Your Adapter")
print("2. Right-click → Update Driver")
print("3. Choose 'Search automatically for drivers'")
print("4. Let Windows find and install updated driver")
print("5. Restart computer")
print("6. Re-pair HC-05")
print()

print("Option B: Install Generic Microsoft Bluetooth Driver")
print("-" * 70)
print("1. Device Manager → Bluetooth → Your Adapter")
print("2. Right-click → Update Driver")
print("3. Choose 'Browse my computer for drivers'")
print("4. Choose 'Let me pick from a list...'")
print("5. Select 'Generic Bluetooth Adapter' or 'Microsoft'")
print("6. Install and restart")
print()

print("=" * 70)
print("SOLUTION 4: Use USB Bluetooth Adapter (MOST RELIABLE)")
print("=" * 70)
print()
print("Modern laptop Bluetooth often has poor Classic BT support.")
print("A USB Bluetooth dongle with SPP support will solve this:")
print()
print("Recommended adapters (~$15-25):")
print("  • Plugable USB-BT4LE")
print("  • ASUS USB-BT400")
print("  • TP-Link UB400")
print()
print("These have better Classic Bluetooth SPP support!")
print()

print("=" * 70)
print("IMMEDIATE ACTION STEPS")
print("=" * 70)
print()
print("Do these in order:")
print()
print("1. Try PuTTY first (fastest test)")
print("   → Download and install PuTTY")
print("   → Try connecting to COM4-COM14 at 9600 baud")
print("   → If data appears, use that COM port in dashboard")
print()
print("2. If PuTTY doesn't work, update Bluetooth driver")
print("   → Device Manager → Update driver")
print("   → Restart PC")
print("   → Re-pair HC-05")
print()
print("3. If still not working, consider USB Bluetooth adapter")
print("   → Much more reliable for Classic Bluetooth devices")
print("   → Plug and play solution")
print()

print("=" * 70)
print("TESTING TOOLS I CAN PROVIDE")
print("=" * 70)
print()
print("Would you like me to:")
print("  A) Create a PuTTY connection script")
print("  B) Create a driver update guide")
print("  C) Help you use your phone instead (already working!)")
print()
print("Your choice? (or just try PuTTY manually first)")
print("=" * 70)

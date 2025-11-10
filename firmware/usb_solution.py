"""
Dashboard Setup Guide - Use USB Instead of Bluetooth
Connect dashboard directly to Pico via USB (COM11)
"""

print("=" * 70)
print("DASHBOARD → PICO USB CONNECTION (BYPASS BLUETOOTH)")
print("=" * 70)
print()

print("Since Windows Bluetooth SPP doesn't work reliably,")
print("let's connect the dashboard DIRECTLY to your Pico via USB!")
print()

print("ADVANTAGES:")
print("  ✅ No Bluetooth issues")
print("  ✅ More reliable connection")
print("  ✅ Faster data transfer")
print("  ✅ No pairing needed")
print()

print("=" * 70)
print("STEP 1: Update Pico Firmware for USB Output")
print("=" * 70)
print()

print("We need to modify the Pico code to send data to BOTH:")
print("  • Bluetooth (for your phone)")
print("  • USB Serial (for dashboard)")
print()

print("The fix is simple - add USB output to your voltage.py")
print()

print("=" * 70)
print("STEP 2: Connect Dashboard to COM11")
print("=" * 70)
print()

print("Once the firmware is updated:")
print()
print("1. Make sure Pico is connected via USB (COM11)")
print("2. Open dashboard: http://127.0.0.1:8000")
print("3. Click 'Connect' or 'Settings'")
print("4. Select port: COM11")
print("5. Set baud rate: 115200 (USB is faster than Bluetooth)")
print("6. Click 'Connect'")
print("7. You'll see real-time voltage data!")
print()

print("=" * 70)
print("BENEFITS OF THIS APPROACH:")
print("=" * 70)
print()

print("✅ HC-05 → Phone (works perfectly)")
print("✅ USB → Dashboard (reliable, no Bluetooth issues)")
print("✅ Both work simultaneously!")
print("✅ No Windows Bluetooth driver problems")
print()

print("=" * 70)
print("READY TO IMPLEMENT?")
print("=" * 70)
print()

print("I can modify your voltage.py to output to BOTH:")
print("  • Bluetooth (for phone monitoring)")
print("  • USB Serial (for dashboard)")
print()

print("This way you get the best of both worlds!")
print()
print("=" * 70)

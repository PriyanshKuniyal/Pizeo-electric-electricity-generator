"""
ACS712 Sensor Test - Raw voltage monitoring
This will help diagnose if the sensor is working or damaged.
"""
import machine
import time

# Read sensor output on GP26
adc = machine.ADC(26)

print("ACS712 Sensor Diagnostic Test")
print("Monitoring raw sensor output voltage on GP26")
print("Expected behavior:")
print("  - No current: ~1.65V (your calibrated zero)")
print("  - With current: voltage should CHANGE")
print()
print("Instructions:")
print("1. Watch the voltage with circuit OPEN (no load)")
print("2. Connect the load - voltage MUST change")
print("3. If voltage never changes, sensor is damaged")
print()
print("Press Ctrl+C to stop")
print("-" * 50)

try:
    while True:
        raw = adc.read_u16()
        voltage = (raw / 65535.0) * 3.3
        
        # Show voltage with more precision for debugging
        print("Raw ADC: {:5d} | Sensor Vout: {:.4f}V".format(raw, voltage))
        
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nTest stopped.")
    print()
    print("Results analysis:")
    print("- If voltage stayed at ~1.65V: Sensor not detecting current")
    print("- If voltage changed: Sensor works, check calibration")
    print("- If voltage is 0V or 3.3V: Wiring issue")

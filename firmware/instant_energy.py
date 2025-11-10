"""
Instantaneous Energy Monitor (Voltage-only)
Shows instantaneous power and energy per measurement interval
Perfect for piezo-electric generator testing
"""
import machine
import time

# CONFIGURATION - Change these for your setup
ADC_PIN = 27  # GPIO pin for voltage measurement
LOAD_OHMS = 1000.0  # Your load resistance in Ohms (REQUIRED!)
INTERVAL_MS = 10  # Measurement interval in milliseconds (10ms = 1/100th second)

# Initialize ADC
adc = machine.ADC(ADC_PIN)

print("Instantaneous Energy Monitor")
print("=" * 60)
print(f"ADC Pin: GP{ADC_PIN}")
print(f"Load: {LOAD_OHMS} Ω")
print(f"Interval: {INTERVAL_MS} ms ({INTERVAL_MS/1000} s)")
print("=" * 60)
print("Measuring... Ctrl+C to stop")
print()

try:
    while True:
        # Read voltage (averaged)
        total = 0
        samples = 20
        for _ in range(samples):
            total += adc.read_u16()
            time.sleep_ms(1)
        
        raw = total // samples
        voltage = (raw / 65535.0) * 3.3
        
        # Calculate instantaneous power (Watts)
        power_w = (voltage * voltage) / LOAD_OHMS
        power_mw = power_w * 1000
        
        # Calculate instantaneous energy for this interval (Joules)
        interval_s = INTERVAL_MS / 1000.0
        energy_j = power_w * interval_s
        energy_mj = energy_j * 1000  # milliJoules
        
        # Also calculate current (derived from V and R)
        current_a = voltage / LOAD_OHMS
        current_ma = current_a * 1000
        
        # Display
        print(f"V: {voltage:.3f}V | I: {current_ma:.2f}mA | "
              f"P: {power_mw:.2f}mW | E_instant: {energy_mj:.3f}mJ")
        
        time.sleep_ms(INTERVAL_MS)

except KeyboardInterrupt:
    print("\nStopped.")

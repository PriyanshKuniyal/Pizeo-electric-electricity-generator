import machine
import time

class CurrentSensor:
    def __init__(self, adc_gpio: int) -> None:
        """Initialize current sensor on specified GPIO pin (ADC capable)."""
        self._adc = machine.ADC(adc_gpio)
    
    def read_voltage(self) -> float:
        """Read voltage from ADC (0-3.3V range on Pico)."""
        analog_value = self._adc.read_u16()  # 0-65535
        voltage = (analog_value / 65535) * 3.3  # Convert to 0-3.3V
        return voltage
    
    def read_current(self, sensor_type: str = "ACS712-5A") -> float:
        """
        Read current in Amperes based on sensor type.
        
        Sensor Types:
        - ACS712-5A: ±5A range, 185 mV/A sensitivity, 2.5V at 0A
        - ACS712-20A: ±20A range, 100 mV/A sensitivity, 2.5V at 0A
        - ACS712-30A: ±30A range, 66 mV/A sensitivity, 2.5V at 0A
        - INA219: Use I2C instead (this is for analog sensors)
        """
        voltage = self.read_voltage()
        
        # Sensor configurations (V_zero, sensitivity in V/A)
        sensors = {
            "ACS712-5A": (2.5, 0.185),    # 2.5V at 0A, 185mV/A
            "ACS712-20A": (2.5, 0.100),   # 2.5V at 0A, 100mV/A
            "ACS712-30A": (2.5, 0.066),   # 2.5V at 0A, 66mV/A
            "custom": (1.65, 0.1),        # Generic: adjust as needed
        }
        
        if sensor_type in sensors:
            v_zero, sensitivity = sensors[sensor_type]
            current = (voltage - v_zero) / sensitivity
            return current
        else:
            # Default calculation (assume 2.5V at 0A, 0.185 V/A)
            return (voltage - 2.5) / 0.185


# Main program
if __name__ == "__main__":
    print("=" * 50)
    print("Current Sensor Reader - GP28 (ADC2)")
    print("=" * 50)
    print()
    
    # Initialize sensor on GP28
    sensor = CurrentSensor(28)  # GP28 = ADC2
    
    # Select your sensor type
    SENSOR_TYPE = "ACS712-30A"  # ELC-30A uses same specs as ACS712-30A
    print(f"Sensor Type: {SENSOR_TYPE} (ELC-30A)")
    print("Reading current continuously...")
    print("Press Ctrl+C to stop")
    print()
    print("Time (s) | Voltage (V) | Current (A)")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        while True:
            # Read current
            voltage = sensor.read_voltage()
            current = sensor.read_current(SENSOR_TYPE)
            elapsed = time.time() - start_time
            
            # Print in readable format
            print(f"{elapsed:8.2f} | {voltage:11.4f} | {current:10.6f}")
            
            time.sleep(0.5)  # Read every 0.5 seconds
            
    except KeyboardInterrupt:
        print()
        print("=" * 50)
        print("Measurement stopped.")
        print("=" * 50)

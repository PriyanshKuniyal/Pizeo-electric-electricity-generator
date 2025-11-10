"""
Energy Monitor - Voltage-based Power and Energy Calculation
For piezo-electric generator or any circuit with known load resistor.

Measures voltage, calculates:
- Instantaneous power (W)
- Current (A) 
- Cumulative energy (Joules and Wh)
"""
import machine
import time


class EnergyMonitor:
    def __init__(self, adc_gpio: int, load_resistance: float):
        """
        Initialize energy monitor.
        
        Args:
            adc_gpio: GPIO pin for ADC (26, 27, or 28)
            load_resistance: Load resistor value in Ohms
        """
        self._adc = machine.ADC(adc_gpio)
        self._load_r = load_resistance
        self._total_energy_j = 0.0  # Total energy in Joules
        self._last_time = time.ticks_ms()
    
    def _sample_voltage(self, samples: int = 20) -> float:
        """Take multiple samples and average."""
        total = 0
        for _ in range(samples):
            total += self._adc.read_u16()
            time.sleep_ms(5)
        
        raw = total // samples
        voltage = (raw / 65535.0) * 3.3
        return voltage
    
    def read(self):
        """
        Read voltage and calculate power, current, and energy.
        
        Returns:
            dict with voltage, current, power, energy_j, energy_wh
        """
        # Measure voltage
        voltage = self._sample_voltage(samples=20)
        
        # Calculate current and power
        current = voltage / self._load_r if self._load_r > 0 else 0
        power = (voltage * voltage) / self._load_r if self._load_r > 0 else 0
        
        # Calculate energy since last reading
        current_time = time.ticks_ms()
        time_elapsed_s = time.ticks_diff(current_time, self._last_time) / 1000.0
        self._last_time = current_time
        
        # Energy = Power × Time
        energy_increment = power * time_elapsed_s
        self._total_energy_j += energy_increment
        
        # Convert to Watt-hours (1 Wh = 3600 J)
        energy_wh = self._total_energy_j / 3600.0
        
        return {
            'voltage': voltage,
            'current': current,
            'power': power,
            'energy_j': self._total_energy_j,
            'energy_wh': energy_wh,
            'energy_mwh': energy_wh * 1000.0  # milliwatt-hours
        }
    
    def reset_energy(self):
        """Reset cumulative energy counter."""
        self._total_energy_j = 0.0
        self._last_time = time.ticks_ms()


# Main program
if __name__ == "__main__":
    # Configuration - CHANGE THESE VALUES FOR YOUR SETUP
    ADC_PIN = 27              # GP27 for voltage measurement
    LOAD_RESISTANCE = 100.0   # Load resistor in Ohms (change to your actual value)
    UPDATE_INTERVAL = 0.5     # Seconds between readings
    
    print("=" * 60)
    print("Energy Monitor - Voltage-Based Calculation")
    print("=" * 60)
    print(f"ADC Pin: GP{ADC_PIN}")
    print(f"Load Resistance: {LOAD_RESISTANCE} Ohms")
    print(f"Update Rate: {UPDATE_INTERVAL}s")
    print()
    print("Formulas:")
    print("  Current (A) = V / R")
    print("  Power (W) = V² / R")
    print("  Energy (J) = Power × Time")
    print()
    print("Press Ctrl+C to stop and see total energy")
    print("-" * 60)
    
    monitor = EnergyMonitor(adc_gpio=ADC_PIN, load_resistance=LOAD_RESISTANCE)
    
    try:
        while True:
            data = monitor.read()
            
            # Display current readings
            print(
                "V: {:.3f}V | "
                "I: {:.3f}A | "
                "P: {:.3f}W | "
                "Energy: {:.2f}J ({:.4f}mWh)".format(
                    data['voltage'],
                    data['current'],
                    data['power'],
                    data['energy_j'],
                    data['energy_mwh']
                )
            )
            
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("FINAL ENERGY SUMMARY")
        print("=" * 60)
        final = monitor.read()
        print(f"Total Energy: {final['energy_j']:.3f} Joules")
        print(f"            = {final['energy_mwh']:.4f} mWh")
        print(f"            = {final['energy_wh']:.6f} Wh")
        print()
        print("To convert to other units:")
        print(f"  - mAh @ 3.7V: {final['energy_mwh'] / 3.7:.4f} mAh")
        print(f"  - Calories: {final['energy_j'] * 0.239:.4f} cal")
        print("=" * 60)

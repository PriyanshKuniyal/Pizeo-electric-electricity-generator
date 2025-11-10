"""
Piezo-Electric Energy Monitor
Measures voltage and calculates instantaneous power & accumulated energy
Uses only voltage sensor - no current sensor needed!

For piezo generator with known load resistance.
"""
import machine
import time


class PiezoEnergyMonitor:
    def __init__(self, adc_gpio: int, load_resistance: float):
        """
        Initialize energy monitor.
        
        Args:
            adc_gpio: GPIO pin for ADC (e.g., 26, 27, 28)
            load_resistance: Load resistance in Ohms (e.g., 1000 for 1kΩ)
        """
        self._adc = machine.ADC(adc_gpio)
        self._load_r = load_resistance  # Ohms
        
        # Energy tracking
        self._total_energy_j = 0.0  # Joules
        self._last_time = time.ticks_ms()
        
        # Statistics
        self._peak_voltage = 0.0
        self._peak_power = 0.0
        self._sample_count = 0
    
    def _read_voltage(self, samples: int = 20) -> float:
        """Read averaged voltage from ADC."""
        total = 0
        for _ in range(samples):
            total += self._adc.read_u16()
            time.sleep_ms(1)
        
        raw = total // samples
        voltage = (raw / 65535.0) * 3.3
        return voltage
    
    def read_and_calculate(self):
        """
        Read voltage, calculate power and update energy.
        
        Returns:
            dict with voltage, current, power, energy
        """
        # Measure voltage
        voltage = self._read_voltage(samples=20)
        
        # Calculate instantaneous power and current
        # P = V²/R,  I = V/R
        power_w = (voltage * voltage) / self._load_r  # Watts
        current_a = voltage / self._load_r  # Amperes
        
        # Calculate time delta and accumulate energy
        current_time = time.ticks_ms()
        delta_ms = time.ticks_diff(current_time, self._last_time)
        delta_s = delta_ms / 1000.0
        
        # Energy = Power × Time
        energy_delta = power_w * delta_s  # Joules
        self._total_energy_j += energy_delta
        
        self._last_time = current_time
        
        # Update statistics
        if voltage > self._peak_voltage:
            self._peak_voltage = voltage
        if power_w > self._peak_power:
            self._peak_power = power_w
        
        self._sample_count += 1
        
        return {
            'voltage_v': voltage,
            'current_ma': current_a * 1000,  # Convert to mA
            'power_mw': power_w * 1000,  # Convert to mW
            'energy_j': self._total_energy_j,
            'energy_mwh': (self._total_energy_j / 3.6),  # Convert J to mWh
            'peak_v': self._peak_voltage,
            'peak_mw': self._peak_power * 1000
        }
    
    def reset_energy(self):
        """Reset accumulated energy counter."""
        self._total_energy_j = 0.0
        self._peak_voltage = 0.0
        self._peak_power = 0.0
        self._sample_count = 0


class BTSerial:
    """HC-05 Bluetooth UART helper."""
    def __init__(self, uart_id: int = 0, baud: int = 9600, tx_pin: int = 0, rx_pin: int = 1):
        self._uart = machine.UART(uart_id, baudrate=baud, 
                                   tx=machine.Pin(tx_pin), 
                                   rx=machine.Pin(rx_pin))
    
    def send_line(self, s: str):
        try:
            if not s.endswith("\n"):
                s = s + "\n"
            self._uart.write(s)
        except:
            pass


# Main execution
if __name__ == "__main__":
    # Configuration
    ADC_PIN = 27  # GP27 for piezo voltage measurement
    LOAD_RESISTANCE = 1000.0  # 1kΩ load (CHANGE THIS to your actual load!)
    UPDATE_INTERVAL = 0.5  # seconds
    USE_BLUETOOTH = False  # Set True to enable BT streaming
    
    # Initialize monitor
    monitor = PiezoEnergyMonitor(adc_gpio=ADC_PIN, load_resistance=LOAD_RESISTANCE)
    
    # Optional: Bluetooth
    if USE_BLUETOOTH:
        bt = BTSerial(uart_id=0, baud=9600, tx_pin=0, rx_pin=1)
    
    print("=" * 60)
    print("Piezo-Electric Energy Monitor")
    print("=" * 60)
    print(f"ADC Pin: GP{ADC_PIN}")
    print(f"Load Resistance: {LOAD_RESISTANCE:.1f} Ω")
    print(f"Update Rate: {UPDATE_INTERVAL}s")
    print()
    print("Monitoring... Press Ctrl+C to stop and see summary.")
    print("-" * 60)
    
    try:
        while True:
            data = monitor.read_and_calculate()
            
            # Format output
            line = (
                f"V: {data['voltage_v']:.3f}V | "
                f"I: {data['current_ma']:.2f}mA | "
                f"P: {data['power_mw']:.2f}mW | "
                f"E: {data['energy_mwh']:.3f}mWh"
            )
            
            print(line)
            
            # Send over Bluetooth if enabled
            if USE_BLUETOOTH:
                bt.send_line(line)
            
            time.sleep(UPDATE_INTERVAL)
    
    except KeyboardInterrupt:
        # Show summary
        data = monitor.read_and_calculate()
        print("\n" + "=" * 60)
        print("SESSION SUMMARY")
        print("=" * 60)
        print(f"Total Energy Harvested: {data['energy_j']:.6f} Joules")
        print(f"                       {data['energy_mwh']:.3f} mWh")
        print(f"Peak Voltage:          {data['peak_v']:.3f} V")
        print(f"Peak Power:            {data['peak_mw']:.2f} mW")
        print(f"Samples Collected:     {monitor._sample_count}")
        print("=" * 60)

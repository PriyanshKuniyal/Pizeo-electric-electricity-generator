import machine
import time
       
class VoltageSensor:
    def __init__(self, adc_gpio:int) -> None:
        self._adc = machine.ADC(adc_gpio)

    def _sample_analog(self, duration:float = 0.5, samples:int = 10) -> int:
        """Takes average of analog reading over short period of time."""
        # I've learned that, no matter what duration you take samples over, the min, mean, and max should be the same. So taking these samples rapidly over 1.5 seconds is fine.
        delay:float = duration / samples
        total:int = 0
        for _ in range(samples):
            total = total + self._adc.read_u16()
            time.sleep(delay)
        return int(round(total / samples, 0))

    def voltage(self, duration:float = 0.5, samples:int = 10) -> float:
        """Burst-samples analog reading and converts to voltage estimate."""
        analog:int = self._sample_analog(duration, samples)
        max_analog:int = 65535
        min_analog:int = 600
        max_voltage:float = 16.3
        min_voltage:float = 0.0
        TR:float = ((analog - min_analog) / (max_analog - min_analog)) * (max_voltage - min_voltage)
        TR = min(max(TR, min_voltage), max_voltage)
        return TR


# Run continuously and print voltage, power, and energy when executed directly.
if __name__ == "__main__":
    # --- CONFIGURATION ---
    LOAD_RESISTANCE = 1000.0  # Ohms - CHANGE THIS to your actual load!
    INTERVAL_S = 0.5  # Time interval: 0.5s = 2 readings per second (slower for Bluetooth)
    USE_BLUETOOTH = True  # Set False to disable BT
    
    # --- Bluetooth (HC-05) over UART helper ---
    class BTSerial:
        def __init__(self, uart_id: int = 1, baud: int = 9600, tx_pin: int = 4, rx_pin: int = 5) -> None:
            # UART1 on Pico: TX=GP4, RX=GP5 (Changed from UART0 GP0/GP1)
            self._uart = machine.UART(uart_id, baudrate=baud, tx=machine.Pin(tx_pin), rx=machine.Pin(rx_pin))

        def send_line(self, s: str) -> None:
            try:
                # Ensure newline termination for most terminal apps
                if not s.endswith("\n"):
                    s = s + "\n"
                self._uart.write(s)
            except Exception:
                # Ignore transient UART errors so the loop continues
                pass

    sensor = VoltageSensor(adc_gpio=27)  # GP27/ADC1 by default
    
    if USE_BLUETOOTH:
        bt = BTSerial(uart_id=1, baud=9600, tx_pin=4, rx_pin=5)  # UART1 GP4/GP5 (working pins!)
    
    # Energy accumulator
    total_energy_j = 0.0
    
    print("Voltage, Power & Energy Monitor")
    print("Load: {} Ohms | Interval: {}s".format(LOAD_RESISTANCE, INTERVAL_S))
    print("-" * 60)
    
    try:
        while True:
            # Measure voltage
            v = sensor.voltage(duration=0.01, samples=10)
            
            # Calculate instantaneous power: P = V²/R
            power_w = (v * v) / LOAD_RESISTANCE
            power_mw = power_w * 1000
            
            # Calculate instantaneous energy for this interval: E = P × Δt
            energy_instant_j = power_w * INTERVAL_S
            energy_instant_mj = energy_instant_j * 1000
            
            # Accumulate total energy
            total_energy_j += energy_instant_j
            total_energy_mwh = total_energy_j / 3.6  # Convert J to mWh
            
            # Format output
            msg = "V: {:.3f}V | P: {:.2f}mW | E_inst: {:.3f}mJ | E_total: {:.3f}mWh".format(
                v, power_mw, energy_instant_mj, total_energy_mwh
            )
            
            print(msg)  # USB serial
            
            if USE_BLUETOOTH:
                bt.send_line(msg)  # Bluetooth
            
            time.sleep(INTERVAL_S)
    except KeyboardInterrupt:
        print("\nStopped. Total energy harvested: {:.6f} J ({:.3f} mWh)".format(
            total_energy_j, total_energy_mwh
        ))
    
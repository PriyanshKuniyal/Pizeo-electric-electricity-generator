"""
Demo script that simulates Raspberry Pi sensor data
This is useful for testing the dashboard without actual hardware
"""
import serial
import time
import random
import sys

def simulate_piezoelectric_data(port='COM3', baudrate=9600):
    """
    Simulate piezoelectric sensor data for testing
    Connect this to a virtual COM port for testing
    """
    try:
        # For testing without hardware, you can use virtual serial ports
        # Windows: com0com, Linux: socat
        print(f"Attempting to connect to {port} at {baudrate} baud...")
        print("Note: This is a demo script. For actual testing without hardware,")
        print("use virtual serial port software like com0com (Windows) or socat (Linux)")
        print()
        
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port}")
        
        # Simulation parameters
        base_voltage = 2.5
        steps = 0
        led_state = "OFF"
        
        while True:
            # Simulate varying voltage based on "steps"
            voltage_variation = random.uniform(-0.5, 0.5)
            voltage = base_voltage + voltage_variation
            
            # Simulate step detection (random chance)
            if random.random() < 0.1:  # 10% chance of step per reading
                steps += 1
            
            # Calculate energy and power (simplified)
            energy = voltage * voltage * 0.0001 * steps
            power = voltage * voltage * 0.0001
            
            # Toggle LED randomly
            if random.random() < 0.15:  # 15% chance to toggle LED
                led_state = "ON" if led_state == "OFF" else "OFF"
            
            # Format data as expected by the dashboard
            data = f"""Voltage: {voltage:.2f}
Energy: {energy:.6f}
Steps: {steps}
Power: {power:.5f}
LED: {led_state}

------------------------------
"""
            
            # Send data
            ser.write(data.encode('utf-8'))
            print(f"Sent: V={voltage:.2f}V, E={energy:.6f}J, Steps={steps}, P={power:.5f}W, LED={led_state}")
            
            # Wait ~0.5 seconds
            time.sleep(0.5)
            
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        print("\nFor testing without hardware:")
        print("1. Windows: Install com0com and create virtual port pair")
        print("2. Linux/Mac: Use socat to create virtual serial ports")
        print("3. Update the port in this script and the dashboard")
    except KeyboardInterrupt:
        print("\nStopping simulation...")
    finally:
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 'COM3'
    simulate_piezoelectric_data(port)

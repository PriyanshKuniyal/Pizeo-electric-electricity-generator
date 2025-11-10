# Bluetooth Echo Test - Two-way communication test
# Pico will echo back anything you type on your phone
# Run: mpremote connect COM11 run "firmware/bt_echo_test.py"

import machine
import time

# Configure UART1 for HC-05 (GP4 = TX, GP5 = RX)
uart = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))

print("Bluetooth Echo Test - UART1 (GP4/GP5)")
print("Type anything on your phone and I'll echo it back!")
print("-" * 60)

# Send initial greeting
uart.write("=== Pico Bluetooth Echo Test ===\n")
uart.write("Type something and I'll echo it back!\n")
uart.write("-" * 40 + "\n")

count = 0
while True:
    # Check if data received from phone
    if uart.any():
        received = uart.read()
        if received:
            msg = received.decode('utf-8', 'ignore').strip()
            print(f"Received from phone: {msg}")
            
            # Echo back to phone
            response = f"Echo #{count}: {msg}\n"
            uart.write(response)
            print(f"Sent to phone: {response.strip()}")
            count += 1
    
    # Send periodic status message every 5 seconds
    time.sleep(0.1)

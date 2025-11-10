# Test Bluetooth HC-05 Transmission
# This sends simple test messages repeatedly
# Run: mpremote connect COM11 run "firmware/test_bt_transmission.py"

import machine
import time

# Configure UART for HC-05 (GP4 = TX, GP5 = RX) - UART1
uart = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))

print("HC-05 Test - Sending data every second")
print("Connect your phone to HC-05 and check if messages appear")
print("-" * 50)

count = 0
while True:
    # Send message via Bluetooth
    msg = f"TEST MESSAGE #{count}\n"
    uart.write(msg)
    
    # Also print to USB for verification
    print(f"Sent: {msg.strip()}")
    
    count += 1
    time.sleep(1)

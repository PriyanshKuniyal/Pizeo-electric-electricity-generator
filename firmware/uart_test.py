"""
Simple UART TX test - sends "HELLO" repeatedly on UART0
Use this to verify UART output with a logic analyzer or oscilloscope
Or connect GP0 back to GP1 (loopback) to test
"""
import machine
import time

# UART0: TX=GP0, RX=GP1
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(0), rx=machine.Pin(1))

print("UART Test - sending 'HELLO' every second on GP0")
print("Connect GP0 to HC-05 RX")
print()

count = 0
while True:
    msg = f"HELLO {count}\n"
    uart.write(msg)
    print(f"Sent: {msg.strip()}")
    count += 1
    time.sleep(1)

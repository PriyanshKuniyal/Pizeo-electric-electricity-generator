import serial
import time

# Replace COM3 with your port (Windows) or /dev/ttyACM0 (Mac/Linux)
ser = serial.Serial('COM12', 115200, timeout=1)

time.sleep(2)  # wait for Pico to reset

ser.write(b'print("Hello Pico via COM!")\r\n')

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(line)

"""
HC-05 Aggressive Multi-Port Monitor
Continuously monitors ALL Bluetooth COM ports simultaneously
Catches data even during brief HC-05 connections
"""
import serial
import threading
import time
import queue

# All your Bluetooth COM ports
BT_PORTS = ["COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10", "COM13", "COM14"]
data_queue = queue.Queue()
active_ports = {}

def monitor_port(port):
    """Monitor a single port continuously"""
    while True:
        try:
            ser = serial.Serial(port, 9600, timeout=0.1)
            ser.dtr = True
            ser.rts = False
            
            if port not in active_ports:
                active_ports[port] = True
                data_queue.put(f"[{port}] OPENED")
            
            while True:
                if ser.in_waiting > 0:
                    try:
                        line = ser.readline().decode(errors='ignore').strip()
                        if line:
                            data_queue.put(f"[{port}] {line}")
                    except:
                        pass
                time.sleep(0.01)
                
        except serial.SerialException:
            if port in active_ports:
                del active_ports[port]
            time.sleep(0.5)  # Wait before retry
        except Exception:
            time.sleep(0.5)

print("HC-05 Aggressive Multi-Port Monitor")
print("=" * 70)
print("Monitoring ALL Bluetooth ports simultaneously...")
print("This will catch data even if HC-05 briefly connects/disconnects")
print("=" * 70)
print()

# Start a thread for each port
threads = []
for port in BT_PORTS:
    t = threading.Thread(target=monitor_port, args=(port,), daemon=True)
    t.start()
    threads.append(t)

# Display data from queue
try:
    while True:
        try:
            msg = data_queue.get(timeout=0.1)
            print(msg)
        except queue.Empty:
            pass
        
        # Show status every 5 seconds
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\n\nStopped.")
    print(f"\nActive ports during session: {list(active_ports.keys())}")

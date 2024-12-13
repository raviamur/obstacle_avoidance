import serial
import time

# Replace '/dev/ttyUSB0' with the actual port your ESP32 is connected to
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

time.sleep(2)  # Allow time for the ESP32 to initialize

while True:
    ser.write(b'Hello ESP32\n')  # Send data to ESP32
    response = ser.readline().decode('utf-8').strip()  # Read the response
    if response:
        print(f"ESP32 says: {response}")
    time.sleep(1)  # Send data every second
import cv2
from rplidar import RPLidar, RPLidarException
import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter backend instead of Qt
import matplotlib.pyplot as plt
import numpy as np

# LIDAR Configuration
LIDAR_PORT = '/dev/ttyUSB0'  # Replace with your LIDAR port
lidar = RPLidar(LIDAR_PORT)
serial_conn = lidar._serial_port  # `_serial_port` is the underlying pyserial object
# Initialize Camera
camera = cv2.VideoCapture(0)

# Plot setup for LIDAR
plt.ion()  # Interactive mode on
fig, ax = plt.subplots(figsize=(6, 6))
lidar_scatter, = ax.plot([], [], 'bo')
ax.set_xlim(-5000, 5000)
ax.set_ylim(-5000, 5000)
ax.set_title("LIDAR Data")

def update_lidar():
    
    scan = next(lidar.iter_scans(max_buf_meas=1000))
    angles, distances = [], []
    for (_, angle, distance) in scan:
        angles.append(np.radians(angle))
        distances.append(distance)
    x = [dist * np.cos(ang) for ang, dist in zip(angles, distances)]
    y = [dist * np.sin(ang) for ang, dist in zip(angles, distances)]
    lidar_scatter.set_data(x, y)
    plt.pause(0.1)
    plt.draw()
   

def update_camera():
    ret, frame = camera.read()
    if ret:
        cv2.imshow('Camera Feed', frame)
        cv2.waitKey(1)
        plt.pause(1.3)
    
while True: 
    try:
        update_lidar()
    except RPLidarException:
        #lidar.stop()
        #lidar.disconnect()
        #lidar = RPLidar(LIDAR_PORT)    
        serial_conn.reset_input_buffer()  # Clears the input buffer
        serial_conn.reset_output_buffer()  # Clears the output buffer
        update_camera()
    except KeyboardInterrupt:
        print("Stopping...")
        break
camera.release()
cv2.destroyAllWindows()

import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter backend in
import matplotlib.pyplot as plt
from rplidar import RPLidar
import cv2
import numpy as np

# LIDAR Configuration
LIDAR_PORT = '/dev/ttyUSB0'
lidar = RPLidar(LIDAR_PORT)

# Initialize Camera
camera = cv2.VideoCapture(0)

# Plot setup for LIDAR
plt.ion()   # Interactive mode on
fig, ax = plt.subplots(figsize=(6, 6))
lidar_scatter, = ax.plot([], [], 'bo')
ax.set_xlim(-5000, 5000)
ax.set_ylim(-5000, 5000)
ax.set_title("LIDAR Data")
try:
    for scan in lidar.iter_scans(max_buf_meas=1000):
        angles = [point[1] for point in scan]
        distances = [point[2] for point in scan]
        lidar_scatter.set_xdata(angles)
        lidar_scatter.set_ydata(distances)
        # ax.relim()
        # ax.autoscale_view()
        
    plt.draw()
    plt.pause(0.01)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    lidar.stop()
    lidar.disconnect()

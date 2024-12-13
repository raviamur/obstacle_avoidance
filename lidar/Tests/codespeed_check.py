from rplidar import RPLidar
import matplotlib
matplotlib.use('TkAgg')  # Use Tkinter backend instead of Qt
import matplotlib.pyplot as plt
import numpy as np
import time

plt.ion()
fig, ax = plt.subplots()
scan_plot, = ax.plot([], [], 'bo')

# LIDAR Configuration
LIDAR_PORT = '/dev/ttyUSB0'  # Replace with your LIDAR port
lidar = RPLidar(LIDAR_PORT)


for scan in lidar.iter_scans():
    start_time = time.time()

    # Process LIDAR data
    angles = [point[1] for point in scan if point[2] > 0]
    distances = [point[2] for point in scan if point[2] > 0]

    # Update plot
    scan_plot.set_xdata(angles)
    scan_plot.set_ydata(distances)
    ax.relim()
    ax.autoscale_view()
    plt.pause(0.01)

    elapsed_time = time.time() - start_time
    print(f"Processing time for one scan: {elapsed_time:.4f} seconds")

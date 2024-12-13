import numpy as np
from rplidar import RPLidar
import matplotlib.pyplot as plt

# LIDAR configuration
LIDAR_PORT = '/dev/ttyUSB0'  # Update with your LIDAR's port
lidar = RPLidar(LIDAR_PORT)

try:
    # Setup Matplotlib plot
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots(figsize=(6, 6))
    scan_plot, = ax.plot([], [], 'bo', markersize=2)  # Initialize scatter plot
    ax.set_xlim(0, 360)
    ax.set_ylim(0, 6000)  # Adjust based on your LIDAR's max range
    ax.set_title("Real-time LIDAR Data")
    ax.set_xlabel("Angle (degrees)")
    ax.set_ylabel("Distance (mm)")

    # Initialize arrays for data
    angles = []
    distances = []

    for new_scan, quality, angle, distance in lidar.iter_measurments():
        if quality > 0:  # Only consider valid measurements
            angles.append(angle)
            distances.append(distance)

        # Update plot for every 100 measurements
        if len(angles) >= 100:
            scan_plot.set_xdata(angles)
            scan_plot.set_ydata(distances)
            ax.relim()
            ax.autoscale_view()
            plt.pause(0.01)

            # Clear the lists for the next batch
            angles = []
            distances = []

except KeyboardInterrupt:
    print("Stopping...")

finally:
    lidar.stop()
    lidar.disconnect()

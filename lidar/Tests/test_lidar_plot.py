import matplotlib.pyplot as plt
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

plt.ion()
fig, ax = plt.subplots()
scan_plot, = ax.plot([], [], 'bo')

try:
    for scan in lidar.iter_scans(max_buf_meas=1000):
        angles = [point[1] for point in scan]
        distances = [point[2] for point in scan]
        scan_plot.set_xdata(angles)
        scan_plot.set_ydata(distances)
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.01)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    lidar.stop()
    lidar.disconnect()

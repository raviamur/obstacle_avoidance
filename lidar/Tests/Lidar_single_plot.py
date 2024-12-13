from rplidar import RPLidar
import matplotlib.pyplot as plt

# LIDAR Configuration
PORT_NAME = '/dev/ttyUSB0'  # Replace with your LIDAR port
lidar = RPLidar(PORT_NAME)

try:
    # Get a single scan
    scan = next(lidar.iter_scans())

    # Extract angles and distances
    angles = [point[1] for point in scan]
    distances = [point[2] for point in scan]

    # Plot the scan
    plt.figure(figsize=(6, 6))
    plt.polar([angle * 3.14159 / 180 for angle in angles], distances, 'o', markersize=2)
    plt.title("LIDAR Single Scan")
    plt.show()

except KeyboardInterrupt:
    print("Stopping...")

finally:
    lidar.stop()
    lidar.disconnect()

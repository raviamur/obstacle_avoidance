import time
from rplidar import RPLidar

LIDAR_PORT = '/dev/ttyUSB0'  # Replace with your LIDAR port
lidar = RPLidar(LIDAR_PORT)

try:
    for scan in lidar.iter_scans():
        start_time = time.time()
        print(f'Scan data: {scan}')
        loop_time = time.time() - start_time
        print(f"Loop execution time: {loop_time:.6f} seconds")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    lidar.stop()
    lidar.disconnect()
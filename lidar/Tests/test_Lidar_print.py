from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'  # Replace with the correct port
lidar = RPLidar(PORT_NAME)

try:
    for scan in lidar.iter_scans():
        print(f'Scan data: {scan}')
except KeyboardInterrupt:
    print("Stopping...")
finally:
    lidar.stop()
    lidar.disconnect()

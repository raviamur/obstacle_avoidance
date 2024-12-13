from rplidar import RPLidar

lidar = RPLidar('/dev/ttyUSB0')  # Replace with your actual port
try:
    for i, scan in enumerate(lidar.iter_scans()):
        print(f'Scan {i}: {scan}')
        if i > 5:
            break
except Exception as e:
    print(f"Error: {e}")
finally:
    lidar.stop()
    lidar.disconnect()

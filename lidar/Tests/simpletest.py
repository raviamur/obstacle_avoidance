from rplidar import RPLidar
lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    #lidar.stop()
   # lidar.reset()
    #lidar.start_motor()
    lidar._serial.reset_input_buffer() 
    print(health)
    print(health)
    if i > 10:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
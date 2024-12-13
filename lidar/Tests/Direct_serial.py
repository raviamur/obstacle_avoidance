from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'  # Replace with the correct port
lidar = RPLidar(PORT_NAME)

# Access the serial connection
serial_conn = lidar._serial_port  # `_serial_port` is the underlying pyserial object

# Check the buffer contents
print("Bytes in buffer:", serial_conn.in_waiting)

# Read raw data from the buffer
raw_data = serial_conn.read(serial_conn.in_waiting)
print("Raw data:", raw_data)
serial_conn.reset_input_buffer()  # Clears the input buffer
serial_conn.reset_output_buffer()  # Clears the output buffer

lidar.stop()
lidar.disconnect()
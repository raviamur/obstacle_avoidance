import cv2
from rplidar import RPLidar, RPLidarException
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
from queue import Queue

matplotlib.use('TkAgg')  # Use Tkinter backend instead of Qt

# LIDAR Configuration
LIDAR_PORT = '/dev/ttyUSB0'  # Replace with your LIDAR port
lidar = RPLidar(LIDAR_PORT)
serial_conn = lidar._serial_port  # `_serial_port` is the underlying pyserial object

# Initialize Camera
camera = cv2.VideoCapture(0)

# Plot setup for LIDAR
plt.ion()  # Interactive mode on
fig, ax = plt.subplots(figsize=(6, 6))
lidar_scatter, = ax.plot([], [], 'bo')
ax.set_xlim(-10000, 10000)
ax.set_ylim(-10000, 10000)
ax.set_title("LIDAR Data")

lidar_running = True
camera_running = True
lidar_data_queue = Queue()

def lidar_thread():
    """Thread function for updating LIDAR data."""
    global lidar_running
    while lidar_running:
        try:
            scan = next(lidar.iter_scans(max_buf_meas=1000))
            angles, distances = [], []
            for (_, angle, distance) in scan:
                angles.append(np.radians(angle))
                distances.append(distance)
            x = [dist * np.cos(ang) for ang, dist in zip(angles, distances)]
            y = [dist * np.sin(ang) for ang, dist in zip(angles, distances)]
            lidar_data_queue.put((x, y))  # add data to queue
            serial_conn.reset_input_buffer()  # Clears the input buffer
            serial_conn.reset_output_buffer()  # Clears the output buffer
        except RPLidarException:
            print("LIDAR exception encountered. Resetting buffers...")
            

def camera_thread():
    """Thread function for updating the camera feed."""
    global camera_running
    while camera_running:
        ret, frame = camera.read()
        if ret:
            cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

try:
    # Start threads for LIDAR and camera
    lidar_thread_obj = threading.Thread(target=lidar_thread, daemon=True)
    camera_thread_obj = threading.Thread(target=camera_thread, daemon=True)

    lidar_thread_obj.start()
    camera_thread_obj.start()

    while True:
        # Update LIDAR plot in the main thread
        if not lidar_data_queue.empty():
            x, y = lidar_data_queue.get()
            lidar_scatter.set_data(x, y)
            plt.pause(0.1)
            plt.draw()
except KeyboardInterrupt:
        print("Stopping...")

finally:
    # Proper cleanup
    lidar_running = False
    camera_running = False
    lidar.stop()
    lidar.disconnect()
    camera.release()
    cv2.destroyAllWindows()
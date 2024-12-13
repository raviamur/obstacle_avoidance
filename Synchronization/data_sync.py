from collections import deque
import cv2
import time
from rplidar import RPLidar, RPLidarException
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import threading
import time
from queue import Queue

# 1. Add Timestamps to Data
# Record the time when LIDAR scans and camera frames are captured.
# Use Python's time.time() for precise timestamps (in seconds since the epoch).
# Capture LIDAR data with timestamp

def get_lidar_data_with_timestamp():
    scan = next(lidar.iter_scans(max_buf_meas=1000))
    timestamp = time.time()
    return scan, timestamp

# Capture camera frame with timestamp
def get_camera_frame_with_timestamp():
    ret, frame = camera.read()
    timestamp = time.time()
    return frame, timestamp if ret else (None, None)

# 2. Store Data Temporarily
# Use queues or lists to temporarily store LIDAR scans and camera frames with their timestamps.
# This ensures you can match the closest timestamps later if needed.

lidar_data_queue = deque(maxlen=10)
camera_data_queue = deque(maxlen=10)
# Append LIDAR data to the queue
scan, lidar_timestamp = get_lidar_data_with_timestamp()
lidar_data_queue.append((lidar_timestamp, scan))

# Append Camera data to the queue
frame, camera_timestamp = get_camera_frame_with_timestamp()
camera_data_queue.append((camera_timestamp, frame))

# 3. Synchronize by Closest Timestamp
# Match LIDAR scans to the nearest camera frame by comparing timestamps.
# If they are close enough (e.g., within 50ms), consider them synchronized.

def find_closest_lidar_to_camera(camera_timestamp, lidar_queue):
    closest_lidar = None
    min_time_diff = float('inf')

    for lidar_timestamp, lidar_scan in lidar_queue:
        time_diff = abs(camera_timestamp - lidar_timestamp)
        if time_diff < min_time_diff:
            closest_lidar = lidar_scan
            min_time_diff = time_diff
    
    return closest_lidar

# 4. Test Synchronization
# Display LIDAR data and the camera frame side by side.
# Include a visual indicator (like overlaying the timestamp) to verify alignment.


def display_synchronized_data(lidar_scan, camera_frame):
    # Overlay timestamps or data onto frames
    combined_display = cv2.hconcat([
        cv2.putText(camera_frame.copy(), "Camera Frame", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2),
        cv2.putText(np.zeros((480, 640, 3), dtype=np.uint8), "LIDAR Data", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    ])
    cv2.imshow('Synchronized Display', combined_display)
    cv2.waitKey(1)

    

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
        except RPLidarException:
            print("LIDAR exception encountered. Resetting buffers...")
            serial_conn.reset_input_buffer()  # Clears the input buffer
            serial_conn.reset_output_buffer()  # Clears the output buffer

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

from collections import deque
import cv2
import time
from rplidar import RPLidar, RPLidarException
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import threading
from queue import Queue

matplotlib.use('TkAgg')  # Use Tkinter backend instead of Qt

# Initialize LIDAR and Camera
LIDAR_PORT = '/dev/ttyUSB0'
lidar = RPLidar(LIDAR_PORT)
serial_conn = lidar._serial_port  # `_serial_port` is the underlying pyserial object
camera = cv2.VideoCapture(0)

# Queues for data
lidar_data_queue = Queue(maxsize=1000)
camera_data_queue = Queue(maxsize=1000)
lidar_data_queue_for_plot = Queue()
# Control flags for threads
lidar_running = threading.Event()
camera_running = threading.Event()
lidar_running.set()
camera_running.set()

# Plot setup for LIDAR
plt.ion()
fig, ax = plt.subplots(figsize=(6, 6))
lidar_scatter, = ax.plot([], [], 'bo')
ax.set_xlim(-10000, 10000)
ax.set_ylim(-10000, 10000)
ax.set_title("LIDAR Data")

def get_lidar_data_with_timestamp():
    scan = next(lidar.iter_scans(max_buf_meas=1000))
    timestamp = time.time()
    return scan, timestamp
    
    # Capture camera frame with timestamp
def get_camera_frame_with_timestamp():
    ret, frame = camera.read()
    timestamp = time.time()
    return frame, timestamp if ret else (None, None)

def lidar_thread():
    """Thread function for updating LIDAR data."""
    while lidar_running.is_set():
        try:
            scan, lidar_timestamp = get_lidar_data_with_timestamp()
            lidar_data_queue.put((lidar_timestamp, scan), block=False)
            angles, distances = [], []
            for (_, angle, distance) in scan:
                angles.append(np.radians(angle))
                distances.append(distance)
            x = [dist * np.cos(ang) for ang, dist in zip(angles, distances)]
            y = [dist * np.sin(ang) for ang, dist in zip(angles, distances)]
            if not lidar_data_queue_for_plot.full():
                lidar_data_queue_for_plot.put((x, y), block=False)
        except RPLidarException:
            #print("LIDAR exception encountered. Resetting buffers...")
            serial_conn.reset_input_buffer()
            serial_conn.reset_output_buffer()
        except Exception as e:
            print(f"LIDAR error: {e}")
            serial_conn.reset_input_buffer()
            serial_conn.reset_output_buffer()
            time.sleep(0.1)

def camera_thread():
    """Thread function for updating the camera feed."""
    while camera_running.is_set():
        try:
            ret, frame = camera.read()
            if ret:
                if not camera_data_queue.full():
                    timestamp = time.time()
                    camera_data_queue.put((timestamp, frame))
               # cv2.imshow('Camera Feed', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                camera_running.clear()  # Stop the thread
        except cv2.error as e:  # Catch OpenCV-specific errors
            print(f"OpenCV error: {e}")
        except Exception as e:  # Catch any other general exceptions
            print(f"Camera error: {e}")



def find_closest_lidar_to_camera(camera_timestamp):
    """Find the closest LIDAR scan to a camera frame."""
    closest_lidar = None
    min_time_diff = float('inf')

    # Convert queue to list for traversal
    lidar_items = list(lidar_data_queue.queue)
    for lidar_timestamp, lidar_scan in lidar_items:
        time_diff = abs(camera_timestamp - lidar_timestamp)
        if time_diff < min_time_diff:
            closest_lidar = lidar_scan
            min_time_diff = time_diff
    return closest_lidar

def display_synchronized_data(lidar_scan, camera_frame):
    """Display synchronized LIDAR and camera data."""
    if camera_frame is None or lidar_scan is None:
        print("No valid data for synchronization")
        return  # Exit if there's no valid data

    try:
        # Create overlay for camera frame
        overlay = camera_frame.copy()
        overlay = cv2.putText(
            overlay,
            "Camera Frame",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        # Placeholder for LIDAR data (can be replaced with actual visualization)
        lidar_overlay = np.zeros_like(overlay)
        lidar_overlay = cv2.putText(
            lidar_overlay,
            "LIDAR Data",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        # Combine the camera frame and LIDAR overlay
        combined_display = cv2.hconcat([overlay, lidar_overlay])

        # Display the combined frame
        if threading.current_thread() is threading.main_thread():
            cv2.imshow('Synchronized Display', combined_display)
            cv2.waitKey(1)  # Ensure GUI events are processed
        else:
            print("cv2.imshow must be called from the main thread.")

    except Exception as e:
        print(f"Error in displaying synchronized data: {e}")
        
try:
    # Start threads for LIDAR and camera
    lidar_thread_obj = threading.Thread(target=lidar_thread, daemon=True)
    camera_thread_obj = threading.Thread(target=camera_thread, daemon=True)

    lidar_thread_obj.start()
    camera_thread_obj.start()

    while True:
        # Update LIDAR plot in the main thread
        if not lidar_data_queue_for_plot.empty():
            x, y = lidar_data_queue_for_plot.get()
            lidar_scatter.set_data(x, y)
            plt.pause(0.1)
            plt.draw()

        # Check for synchronization
        if not camera_data_queue.empty():
            camera_timestamp, camera_frame = camera_data_queue.get()
            
            lidar_scan = find_closest_lidar_to_camera(camera_timestamp)
            display_synchronized_data(lidar_scan, camera_frame)

            time.sleep(0.1)  # Avoid tight loop

except KeyboardInterrupt:
    print("Stopping...")

finally:
    # Proper cleanup
    lidar_running.clear()
    camera_running.clear()
    lidar.stop()
    lidar.disconnect()
    camera.release()
    cv2.destroyAllWindows()

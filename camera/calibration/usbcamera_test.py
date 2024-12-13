import cv2

# Specify the USB camera index (typically /dev/video0 for the first camera)
camera_index = 0  # Adjust this if needed, e.g., 1 for /dev/video1
camera = cv2.VideoCapture(camera_index)

if not camera.isOpened():
    print(f"Error: Unable to open camera at index {camera_index}.")
else:
    print("Press 'q' to quit.")
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()
        if not ret:
            print("Error: Unable to read frame.")
            break
        
        # Display the resulting frame
        cv2.imshow('USB Camera Feed', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the camera and close windows
camera.release()
cv2.destroyAllWindows()

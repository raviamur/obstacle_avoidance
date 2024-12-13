import cv2

# Initialize Camera
camera = cv2.VideoCapture(22)

if not camera.isOpened():
    print("Error: Camera not found or cannot be opened.")
    exit()

def update_camera():
    ret, frame = camera.read()
    if ret:
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            raise KeyboardInterrupt
    else:
        print("Error: Unable to read from camera.")
        raise KeyboardInterrupt

try:
    while True:
        update_camera()
except KeyboardInterrupt:
    print("Stopping...")
finally:
    camera.release()
    cv2.destroyAllWindows()

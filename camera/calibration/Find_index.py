import cv2

index = 0
while True:
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"Camera found at index {index}")
        cap.release()
    else:
        print(f"No camera at index {index}")
    index += 1
    if index > 25:  # Test up to 10 indices
        break

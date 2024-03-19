import cv2
import time

cap = cv2.VideoCapture(0)

start_time = time.time()
frame_count = 0
fps = 0

while True:
    success, frame = cap.read()
    frame_count += 1

    # Calculate FPS
    if frame_count >= 10:  # Update FPS every 10 frames
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()

    # Display FPS on the frame
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Frame', frame)

    # time.sleep(0.25)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import requests
import numpy as np
import time
import asyncio

# Server URL
server_url = 'http://192.168.143.77:5000/summary?format=bin'

cap = cv2.VideoCapture(0)

start_time = time.time()
frame_count = 0
fps = 0

async def main():
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

        # Convert frame to JPEG format
        _, encoded_img = cv2.imencode('.jpg', frame)
        img_bytes = encoded_img.tobytes()

        try:
            # Send frame as a POST request to the server
            response = await requests.post(server_url, data=img_bytes)

            if response.status_code != 200:
                print("Failed to send frame:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error sending frame:", e)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    return None

if __name__ == '__main__':
    asyncio.run(main)


    cap.release()
    cv2.destroyAllWindows()

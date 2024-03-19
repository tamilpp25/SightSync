import cv2
import requests
from threading import Timer
import pyttsx3

# Function to send frame as a POST request
def send_request(server_url, frame):
    # Convert frame to JPEG format
    _, encoded_img = cv2.imencode('.jpg', frame)
    img_bytes = encoded_img.tobytes()

    try:
        # Send frame as a POST request to the server
        response = requests.post(server_url, data=img_bytes)

        if response.status_code != 200:
            print("Failed to send frame:", response.status_code)

        else: 
            text = response.json()['data'] 
            print(text)
            engine.say(text)
            engine.runAndWait()            
            
    except requests.exceptions.RequestException as e:
        print("Error sending frame:", e)

# Function to continuously send requests at regular intervals
def send_continuous_requests(server_url, cap):
    # Read the most recent frame from the camera
    _, frame = cap.read()
    
    # Send the frame as a request
    send_request(server_url, frame)
    
    # Schedule the next request after 5 seconds
    Timer(10, send_continuous_requests, [server_url, cap]).start()

if __name__ == "__main__":
    # Server URL
    server_url = 'http://192.168.137.1:5000/summary?format=bin'

    # Open the camera
    cap = cv2.VideoCapture(0)

    # Flag to track if 's' key has been pressed
    send_flag = False

    engine = pyttsx3.init()

    engine.setProperty('rate', 150)    # Speed of speech (words per minute)
    engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

    while True:
        # Capture a frame from the camera
        success, frame = cap.read()

        # Display the frame
        cv2.imshow('Frame', frame)

        # Check if 's' key is pressed
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            send_flag = True
            print('Request Sent')

        # If 's' key is pressed, start sending continuous requests
        if send_flag:
            send_continuous_requests(server_url, cap)
            send_flag = False  # Reset the flag

        # Exit loop if 'q' key is pressed
        if key & 0xFF == ord('q'):
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

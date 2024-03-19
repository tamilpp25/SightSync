import face_recognition
import cv2

# Load known images (images containing known faces)
known_image = face_recognition.load_image_file("D:/Onedrive/Projects/SightSync/Images/balaji/balaji.jpg")

# Encode known faces
known_encoding = face_recognition.face_encodings(known_image)[0]

# Load an unknown image (image containing unknown faces)
unknown_image = face_recognition.load_image_file("D:/Onedrive/Projects/SightSync/Images/unknown/unknown.jpg")

# Find face locations in the unknown image
face_locations = face_recognition.face_locations(unknown_image)

# Create an RGB copy of the unknown image
rgb_unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)

# Iterate through the detected face locations and draw bounding boxes
for top, right, bottom, left in face_locations:
    cv2.rectangle(rgb_unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)

# Display the output image with bounding boxes
cv2.imshow("Unknown Face with Bounding Box", rgb_unknown_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Encode unknown faces
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

# Compare faces
results = face_recognition.compare_faces([known_encoding], unknown_encoding)

if results[0]:
    print("Face recognized!")
else:
    print("Face not recognized!")

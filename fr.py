import face_recognition
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from payment import confirm_payment
import json

with open('users.json', 'r') as f:
    users = json.load(f)


# Function to update the video feed in the tkinter window
def update_video():
    ret, frame = video_capture.read()
    if not ret:
        return
    
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Show confirmation button if face is recognized
        if name != "Unknown":
            if name == "Jia Yee":
                user = users[0]
            else:
                user = users[1]
            confirm_button.configure(command=lambda : confirm_payment(user, total_price=10))
        else:
            confirm_button.configure(command=None)

    # Convert the frame to a format suitable for displaying in tkinter
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)

    video_label.configure(image=img)
    video_label.image = img
    video_label.after(10, update_video)

# Create a tkinter window
root = tk.Tk()
root.title("Face Payment System")

# Create a label to display the video feed
video_label = tk.Label(root)
video_label.pack()

# Create a confirmation button
confirm_button = tk.Button(root, text="Confirm Payment")
confirm_button.pack(side=tk.BOTTOM, pady=10)


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load diverse images of Jia Yee
jy_image_1 = face_recognition.load_image_file("examples/jy1.jpeg")
jy_image_2 = face_recognition.load_image_file("examples/jy2.jpeg")
jy_image_3 = face_recognition.load_image_file("examples/jy3.jpeg")
jy_image_4 = face_recognition.load_image_file("examples/jy4.jpeg")

# Compute face encodings for each image
jy_face_encoding_1 = face_recognition.face_encodings(jy_image_1)[0]
jy_face_encoding_2 = face_recognition.face_encodings(jy_image_2)[0]
jy_face_encoding_3 = face_recognition.face_encodings(jy_image_3)[0]
jy_face_encoding_4 = face_recognition.face_encodings(jy_image_4)[0]

# Load diverse images of Sabrina
sab_image_1 = face_recognition.load_image_file("examples/sab1.jpg")
sab_image_2 = face_recognition.load_image_file("examples/sab2.jpg")
sab_image_3 = face_recognition.load_image_file("examples/sab3.jpeg")
sab_image_4 = face_recognition.load_image_file("examples/sab4.jpg")
sab_image_5 = face_recognition.load_image_file("examples/sab5.jpg")
sab_image_6 = face_recognition.load_image_file("examples/sab6.jpg")

# Compute face encodings for each image
sab_face_encoding_1 = face_recognition.face_encodings(sab_image_1)[0]
sab_face_encoding_2 = face_recognition.face_encodings(sab_image_2)[0]
sab_face_encoding_3 = face_recognition.face_encodings(sab_image_3)[0]
sab_face_encoding_4 = face_recognition.face_encodings(sab_image_4)[0]
sab_face_encoding_5 = face_recognition.face_encodings(sab_image_5)[0]
sab_face_encoding_6 = face_recognition.face_encodings(sab_image_6)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    jy_face_encoding_1,
    jy_face_encoding_2,
    jy_face_encoding_3,
    jy_face_encoding_4,
    sab_face_encoding_1,
    sab_face_encoding_2,
    sab_face_encoding_3,
    sab_face_encoding_4,
    sab_face_encoding_5,
    sab_face_encoding_6
]

known_face_names = [
    "Jia Yee",
    "Jia Yee",
    "Jia Yee",
    "Jia Yee",
    "Sabrina",
    "Sabrina",
    "Sabrina",
    "Sabrina",
    "Sabrina",
    "Sabrina"
]

# Start updating the video feed
update_video()

# Start the tkinter main loop
root.mainloop()

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

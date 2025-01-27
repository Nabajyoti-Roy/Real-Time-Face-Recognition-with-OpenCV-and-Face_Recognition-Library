import cv2
import face_recognition

# Initialize known faces and names
known_face_encodings = []
known_face_names = []

# Paths to images and their respective names
image_paths = [
    r"C:\Users\nabaj\Face-Recognition-Project\person1.jpg",
    r"C:\Users\nabaj\Face-Recognition-Project\person2.jpg",
    r"C:\Users\nabaj\Face-Recognition-Project\person3.jpg",
    r"C:\Users\nabaj\Face-Recognition-Project\person5.jpg"
]
names = ["Nabayoti Roy", "Soham Lodh", "Abhra Bhowmick", "Shruti Shreya"]

# Load known faces and names
for path, name in zip(image_paths, names):
    try:
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
        else:
            print(f"Warning: No face found in {path}")
    except Exception as e:
        print(f"Error loading image {path}: {e}")

# Check if known faces were loaded
if not known_face_encodings:
    print("No known faces loaded. Exiting...")
    exit()

# Initialize webcam
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Could not access webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame. Exiting...")
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and encodings
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Match each face encoding to known faces
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Scale back up face locations
        top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4

        # Draw rectangle and name label
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Video", frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()

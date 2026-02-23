import cv2

def main():
    # Load the cascade
    # Use the xml file from cv2 data
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # To capture video from webcam. 
    cap = cv2.VideoCapture(0)
    # To use a video file as input 
    # cap = cv2.VideoCapture('filename.mp4')
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Read the frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Add face count
        cv2.putText(frame, f'Faces: {len(faces)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display
        cv2.imshow('Face Detection', frame)

        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k == ord('q'):
            break
        
    # Release the VideoCapture object
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

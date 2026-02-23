import cv2
import random
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

# Load the Haar Cascade for face detection
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

def draw_circular_mesh(frame, x, y, w, h):
    """
    Draws a futuristic circular 'recognition' mesh over a face.
    """
    center_x = x + w // 2
    center_y = y + h // 2
    radius = int(max(w, h) * 0.6)
    
    # 1. Draw the Main Recognition Circle (Glassy/Neon effect)
    # Outer glowing circle
    cv2.circle(frame, (center_x, center_y), radius, (0, 255, 150), 2, cv2.LINE_AA)
    # Thicker segments for a more "tech" look
    start_angle = (pygame_ticks() // 10) % 360 if 'pygame_ticks' in globals() else 0 # Simulation of rotation
    # Actually let's use a simpler static tech circle for now
    for i in range(0, 360, 60):
        cv2.ellipse(frame, (center_x, center_y), (radius+5, radius+5), 0, i, i+20, (0, 255, 150), 3)

    # 2. Draw Landmarks (Dots and connecting lines) in a more structured way
    # Using relative points based on the face box
    pts = [
        (center_x, y + int(h*0.1)),      # Forehead
        (x + int(w*0.25), y + int(h*0.35)), # Left Eye
        (x + int(w*0.75), y + int(h*0.35)), # Right Eye
        (center_x, center_y),            # Nose
        (center_x, y + int(h*0.85)),     # Chin
        (x + int(w*0.2), center_y),      # Left Cheek
        (x + int(w*0.8), center_y),      # Right Cheek
    ]
    
    # Connect dots with lines (Star-like connections but inside a circle)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            # Only connect specific pairs to avoid "star" mess
            if abs(i-j) <= 2:
                cv2.line(frame, pts[i], pts[j], (0, 255, 150), 1, cv2.LINE_AA)
    
    # Draw the dots
    for pt in pts:
        cv2.circle(frame, pt, 4, (0, 255, 150), -1)
        cv2.circle(frame, pt, 6, (0, 255, 150), 1)

    # 3. Add Identification Tag near the circle
    tag_x = center_x + radius + 10
    tag_y = center_y - 20
    cv2.line(frame, (center_x + radius, center_y), (tag_x, tag_y + 10), (0, 255, 150), 1)
    cv2.rectangle(frame, (tag_x, tag_y), (tag_x + 100, tag_y + 20), (0, 0, 0), -1)
    cv2.putText(frame, "VERIFYING...", (tag_x + 5, tag_y + 15), 
                cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 255, 150), 1)

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            draw_circular_mesh(frame, x, y, w, h)
            
            # Add identification tag
            tag_box_y = y - 45 if y - 45 > 0 else y + h + 20
            cv2.rectangle(frame, (x, tag_box_y), (x + 130, tag_box_y + 25), (0, 0, 0), -1)
            cv2.putText(frame, "STATUS: TRACKING", (x + 5, tag_box_y + 18), 
                        cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 255, 150), 1)

        # UI Overlay
        cv2.rectangle(frame, (0, 0), (220, 50), (0, 0, 0), -1)
        cv2.putText(frame, f'RECOGNITION: ACTIVE', (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 150), 1)
        cv2.putText(frame, f'TARGETS: {len(faces)}', (10, 40), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 150), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

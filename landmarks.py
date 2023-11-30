import torch
import cv2
import mediapipe as mp
import numpy as np
import json

cap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawing_spec = mpDraw.DrawingSpec(thickness=1, circle_radius=1, color=(255, 255, 255))

# Scale factor for processing
scale_factor = 3
connections = mpFaceMesh.FACEMESH_TESSELATION

all_landmarks = []
while True:
    success, img = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Scale down the image for faster processing
    img_small = cv2.resize(img, (0, 0), fx=1/scale_factor, fy=1/scale_factor)
    imgRGB = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    blacked_img = np.zeros(img.shape, dtype=np.uint8)

    if results.multi_face_landmarks:
        h, w, c = img.shape
        screen_center = (w // 2, h // 2)

        for faceLms in results.multi_face_landmarks:
            # Calculate face center
            face_x = [lm.x * w for lm in faceLms.landmark]
            face_y = [lm.y * h for lm in faceLms.landmark]
            face_center = (sum(face_x) / len(face_x), sum(face_y) / len(face_y))

            # Transform each landmark point
            scaled_landmarks = []
            for id, lm in enumerate(faceLms.landmark):
                # Shift to center and scale
                shifted_x = (lm.x * w - face_center[0]) + screen_center[0]
                shifted_y = (lm.y * h - face_center[1]) + screen_center[1]

                scaled_x = (shifted_x - screen_center[0]) * scale_factor + screen_center[0]
                scaled_y = (shifted_y - screen_center[1]) * scale_factor + screen_center[1]

                scaled_landmarks.append((int(scaled_x), int(scaled_y)))

                # Draw the landmark point
                cv2.circle(blacked_img, (int(scaled_x), int(scaled_y)), 1, (0, 255, 0), -1)
            all_landmarks.append(scaled_landmarks)
            # Draw connections
            for (start, end) in connections:
                cv2.line(blacked_img, scaled_landmarks[start], scaled_landmarks[end], (255, 255, 255), 1)
    cv2.imshow("Image", blacked_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


with open("landmarks.json", "w") as f:
    json.dump(all_landmarks, f)
cap.release()
cv2.destroyAllWindows()




import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math
import numpy as np
import screen_brightness_control as sbc
import pyautogui
import os
import time

# --- 1. Model Files Download Setup ---
hand_model_path = 'hand_landmarker.task'
face_model_path = 'face_landmarker.task'

if not os.path.exists(hand_model_path):
    print("Downloading hand_landmarker model file...")
    import urllib.request
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, hand_model_path)
    print("Hand model downloaded successfully!")

if not os.path.exists(face_model_path):
    print("Downloading face_landmarker model file...")
    import urllib.request
    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    urllib.request.urlretrieve(url, face_model_path)
    print("Face model downloaded successfully!")

# --- 2. MediaPipe Hand & Face Detectors Setup ---
BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Hand Options
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
hand_options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=hand_model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.6,
    min_hand_presence_confidence=0.6
)
hand_detector = HandLandmarker.create_from_options(hand_options)

# Face Options (For Gender/Face Analysis)
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
face_options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=face_model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_faces=1,
    min_face_detection_confidence=0.6,
    min_face_presence_confidence=0.6
)
face_detector = FaceLandmarker.create_from_options(face_options)

# --- 3. Webcam Initialize ---
cap = cv2.VideoCapture(0)

bright_bar = 400
bright_per = 0

# Variables for tracking
last_screenshot_time = 0
prev_left_hand_y = 0

print("Camera starting... Press 'q' to exit.")

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Camera frame not available.")
        break

    # Frame horizontally flip karein (mirror view)
    img = cv2.flip(img, 1)
    h, w, c = img.shape

    # OpenCV BGR to RGB conversion
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

    # --- 4. Face Detection & Gender Analysis ---
    face_detection_result = face_detector.detect(mp_image)
    detected_gender = "Detecting Face..."
    gender_color = (200, 200, 200)

    if face_detection_result.face_landmarks:
        for face_landmarks in face_detection_result.face_landmarks:
            # Face geometry ke kuch key points (Jawline width, cheekbones, chin height ratio)
            # Jaw left (234), Jaw right (454), Chin (152), Forehead top (10)
            jaw_left = face_landmarks[234]
            jaw_right = face_landmarks[454]
            chin = face_landmarks[152]
            forehead = face_landmarks[10]

            # Face width & height calculate karna
            face_width = math.hypot((jaw_right.x - jaw_left.x) * w, (jaw_right.y - jaw_left.y) * h)
            face_height = math.hypot((chin.x - forehead.x) * w, (chin.y - forehead.y) * h)

            ratio = face_width / face_height if face_height > 0 else 0

            # Heuristic rule based on facial structure ratios (approximate landmark mapping)
            # Typically, facial proportions vary slightly; this serves as a geometric estimator
            if ratio > 0.78:
                detected_gender = "BOY (Male)"
                gender_color = (255, 100, 0)
            else:
                detected_gender = "GIRL (Female)"
                gender_color = (203, 192, 255)

    # --- 5. Hand Detection (Brightness, Screenshot & Sign Language) ---
    hand_detection_result = hand_detector.detect(mp_image)

    sign_meaning = "Waiting for Sign..."
    display_status = False
    left_hand_found = False

    if hand_detection_result.hand_landmarks:
        for hand_landmarks in hand_detection_result.hand_landmarks:
            
            wrist_x = hand_landmarks[0].x * w

            # Count extended fingers
            tips = [4, 8, 12, 16, 20]  
            pips = [3, 6, 10, 14, 18] 
            
            extended = []
            if hand_landmarks[4].x > hand_landmarks[3].x:
                extended.append(1)
            else:
                extended.append(0)
                
            extended_count = 0
            for i in range(1, 5):
                if hand_landmarks[tips[i]].y < hand_landmarks[pips[i]].y:
                    extended.append(1)
                    extended_count += 1
                else:
                    extended.append(0)

            # ==========================================
            # A. RIGHT SIDE HAND -> BRIGHTNESS & SIGN LANGUAGE
            # ==========================================
            if wrist_x > w / 2:  
                
                # Brightness Control
                x1, y1 = int(hand_landmarks[4].x * w), int(hand_landmarks[4].y * h)
                x2, y2 = int(hand_landmarks[8].x * w), int(hand_landmarks[8].y * h)

                cv2.circle(img, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 8, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

                length = math.hypot(x2 - x1, y2 - y1)

                bright_level = np.interp(length, [25, 250], [0, 100])
                bright_bar = np.interp(length, [25, 250], [400, 150])
                bright_per = np.interp(length, [25, 250], [0, 100])

                bright_level = max(0, min(100, bright_level))
                bright_per = max(0, min(100, bright_per))

                try:
                    sbc.set_brightness(int(bright_level))
                except Exception as e:
                    pass

                # Sign Language Recognition
                if extended == [1, 0, 0, 0, 0] and hand_landmarks[4].y < hand_landmarks[3].y:
                    sign_meaning = "YES / GOOD"
                elif extended == [1, 1, 1, 1, 1]:
                    sign_meaning = "HELLO / STOP"
                elif extended == [0, 0, 0, 0, 0]:
                    sign_meaning = "READY / STRONG"
                elif extended == [0, 1, 1, 0, 0]:
                    sign_meaning = "PEACE / VICTORY"
                elif extended == [0, 1, 0, 0, 0]:
                    sign_meaning = "ATTENTION"

            # ==========================================
            # B. LEFT SIDE HAND -> TOP-TO-BOTTOM SCREENSHOT
            # ==========================================
            elif wrist_x <= w / 2:  
                left_hand_found = True
                current_wrist_y = hand_landmarks[0].y

                if extended_count >= 3 and prev_left_hand_y != 0:
                    movement_delta = current_wrist_y - prev_left_hand_y
                    
                    if movement_delta > 0.03:  
                        current_time = time.time()
                        if current_time - last_screenshot_time > 2.0:
                            screenshot = pyautogui.screenshot()
                            timestamp = int(time.time())
                            filename = f"screenshot_{timestamp}.png"
                            screenshot.save(filename)
                            print(f"Screenshot saved as {filename}")
                            last_screenshot_time = current_time

                prev_left_hand_y = current_wrist_y

    if not left_hand_found:
        prev_left_hand_y = 0


    # --- 6. UI RENDERING ---
    # Screenshot alert notification
    if time.time() - last_screenshot_time < 1.5:
        cv2.putText(img, "SCREENSHOT TAKEN!", (int(w/2) - 180, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

    # Brightness Bar UI (Left side)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(bright_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(bright_per)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)

    # Top-Right Corner: Sign Language Display Box
    cv2.rectangle(img, (w - 280, 10), (w - 10, 80), (50, 50, 50), cv2.FILLED)
    cv2.rectangle(img, (w - 280, 10), (w - 10, 80), (0, 255, 0), 2)
    cv2.putText(img, "Sign Meaning:", (w - 270, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    cv2.putText(img, f"{sign_meaning}", (w - 270, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Bottom Display: Face/Gender Analysis Text
    cv2.rectangle(img, (int(w/2) - 160, h - 70), (int(w/2) + 160, h - 20), (30, 30, 30), cv2.FILLED)
    cv2.rectangle(img, (int(w/2) - 160, h - 70), (int(w/2) + 160, h - 20), (255, 255, 255), 1)
    cv2.putText(img, f"Face: {detected_gender}", (int(w/2) - 145, h - 38), cv2.FONT_HERSHEY_SIMPLEX, 0.65, gender_color, 2)

    cv2.imshow("Complete Gesture & Face Analysis Project", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
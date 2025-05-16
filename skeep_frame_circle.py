import cv2
import mediapipe as mp
import csv
import time
import numpy as np
import os
#same as skeep_frame but with circle
# מודול Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# נתיב קובץ הוידאו
video_path = r'C:\Users\Admin\FinalProject\video1.mp4'
print(f"נתיב קובץ הווידאו: {video_path}")

# פתיחת הוידאו
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("שגיאה בפתיחת קובץ הווידאו. בדוק את הנתיב: ", video_path)
    exit()

# פרטי וידאו
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print(f"Total frames: {total_frames}, FPS: {fps}")

# תיקייה לשמירת הקבצים
output_dir = r'C:\Users\Admin\FinalProject'

# פתיחת קובץ CSV
csv_path = os.path.join(output_dir, 'video1.csv')
csv_file = open(r'C:\Users\Admin\FinalProject\video1.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Frame", "Hand", "Landmark", "X", "Y", "Z"])

# קובץ וידאו לפלט
output_video_path = r'C:\Users\Admin\FinalProject\output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

start_time = time.time()
frame_index = 0

# --- פונקציה לציור עיגולים ---
def draw_hand_volume_circles(image, landmarks, width, height):
    for i, landmark in enumerate(landmarks.landmark):
        x_px = int(landmark.x * width)
        y_px = int(landmark.y * height)

        # חישוב רדיוס לפי מרחק משכנים (פשוט, רק דוגמה)
        neighbors = []
        if i > 0:
            neighbors.append(landmarks.landmark[i - 1])
        if i < 20:
            neighbors.append(landmarks.landmark[i + 1])

        dists = [np.sqrt((landmark.x - n.x)**2 + (landmark.y - n.y)**2) for n in neighbors]
        avg_dist = np.mean(dists) if dists else 0.01
        radius_px = int(avg_dist * width * 0.5)  # קנה מידה

        # ציור העיגול
        cv2.circle(image, (x_px, y_px), radius_px, (0, 255, 0), 2)

# --- לולאת פריימים ---
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("סיום הסרטון או שגיאה בקריאה.")
        break

    if frame_index % 3 == 0:
        print(f"מסגרת: {frame_index}")

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # כתיבה ל־CSV
                for landmark_index, landmark in enumerate(hand_landmarks.landmark):
                    csv_writer.writerow([frame_index, hand_index, landmark_index, landmark.x, landmark.y, landmark.z])

                # ציור החיבורים
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # ציור עיגולים
                draw_hand_volume_circles(image, hand_landmarks, frame_width, frame_height)

        # כתיבת הפריים המעובד
        out.write(image)

    frame_index += 1

# ניקוי משאבים
cap.release()
out.release()
cv2.destroyAllWindows()
csv_file.close()

elapsed_time = time.time() - start_time
print(f"העיבוד הסתיים. זמן כולל: {elapsed_time:.2f} שניות.")
print(f"קורדינאטות נשמרו כ־'{csv_path}', וידאו כ־'{output_video_path}'")

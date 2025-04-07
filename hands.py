import cv2
import mediapipe as mp
import csv
import time  # הוספת מודול זמן

# הגדרת מודול ה-Hands של Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# הגדרת נתיב קובץ הוידאו
video_path = '/home/yona/Project/video1.mp4'
print(f"נתיב קובץ הווידאו: {video_path}")

# פתח את קובץ הוידאו
cap = cv2.VideoCapture(video_path)

# בדוק אם קובץ הווידאו נפתח בהצלחה
if not cap.isOpened():
    print("שגיאה בפתיחת קובץ הווידאו. בדוק את הנתיב: ", video_path)
    exit()

# הדפסת מידע על הווידאו
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Total frames: {total_frames}, FPS: {fps}")

# פתיחת קובץ CSV לכתיבת קורדינאטות
csv_file = open('/home/yona/Project/hands_coordinates.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

# כתיבת כותרות לקובץ ה-CSV
csv_writer.writerow(["Frame", "Hand", "Landmark", "X", "Y", "Z"])

# הגדרת קובץ הפלט לוידאו
output_video_path = '/home/yona/Project/output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # קודק ליצירת קובץ MP4
out = cv2.VideoWriter(output_video_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))  # הגדרת וידאו

# התחלת מדידת זמן
start_time = time.time()

frame_index = 0
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("שגיאה בטעינת המסגרות מהוידאו או סיום הסרטון")
        break

    print(f"עיבוד מסגרת מספר: {frame_index}")

    # המרת התמונה ל-RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # זיהוי נקודות ידיים
    results = hands.process(image_rgb)

    # ציור נקודות הידיים על המסגרת וכתיבת קורדינאטות ל-CSV
    if results.multi_hand_landmarks:
        for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            for landmark_index, landmark in enumerate(hand_landmarks.landmark):
                # חשב את הקורדינאטות היחסיות (X, Y, Z)
                x = landmark.x
                y = landmark.y
                z = landmark.z
                # כתוב את הנתונים לקובץ ה-CSV
                csv_writer.writerow([frame_index, hand_index, landmark_index, x, y, z])

            # ציור הנקודות והחיבורים על התמונה
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # כתיבת המסגרת המעובדת לקובץ הווידאו
    out.write(image)

    frame_index += 1

# סיום מדידת זמן
end_time = time.time()
elapsed_time = end_time - start_time

# שחרור משאבים וסגירת קבצים
cap.release()
out.release()
cv2.destroyAllWindows()
csv_file.close()

print(f"עיבוד הווידאו הסתיים. זמן העיבוד הכולל: {elapsed_time:.2f} שניות.")
print(f"קובץ הקורדינאטות נשמר ב-{csv_file.name}, וקובץ הווידאו נשמר ב-{output_video_path}.")

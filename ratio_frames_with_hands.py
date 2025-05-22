import pandas as pd
import os
from datetime import timedelta, datetime, time
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import seaborn as sns


# Settings
fps = 29.655
excel_path = r'C:\Users\Admin\FinalProject\Data_base.xlsx'
csv_dir = r'C:\Users\Admin\FinalProject\csv'
output_path = excel_path  # ידרוס את הקובץ המקורי
# --- Heatmap של כל הנקודות מכל הסרטונים --- #
all_x = []
all_y = []
# Step 1: Read Excel
df = pd.read_excel(excel_path)

# 🔍 המרת length לזמן
df['length'] = pd.to_timedelta(df['length'], errors='coerce')

# פונקציה להמרת זמן לשניות
def convert_time_to_seconds(time_obj):
    if isinstance(time_obj, timedelta):
        return time_obj.total_seconds()
    elif isinstance(time_obj, datetime):
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    elif isinstance(time_obj, time):
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    return 0

# חישוב מספר פריימים
df['num_frames'] = df['length'].apply(convert_time_to_seconds) * fps

# רשימות לאיסוף תוצאות
ratios = []
avg_areas = []
center_distances = []

# ---- חישוב שטח יד ---- #
def compute_radius_area(df_frame):
    area_total = 0.0
    for i in range(21):
        point = df_frame[df_frame['Landmark'] == i]
        if len(point) == 0:
            continue
        x, y = point.iloc[0][['X', 'Y']]
        neighbors = df_frame[(df_frame['Landmark'].isin([i - 1, i + 1]))]
        if len(neighbors) == 0:
            continue
        neighbor_coords = neighbors[['X', 'Y']].values
        dists = np.linalg.norm(neighbor_coords - np.array([x, y]), axis=1)
        avg_radius = np.mean(dists)
        area_total += pi * (avg_radius ** 2)
    return area_total

def compute_area_per_frame(df):
    result = []
    for frame_id, df_frame in df.groupby('Frame'):
        area = compute_radius_area(df_frame)
        if not np.isnan(area):
            result.append(area)
    if not result:
        return np.nan
    return np.nanmean(result)

def compute_mean_center_distance(df):
    result = []
    for frame_id, df_frame in df.groupby('Frame'):
        distances = []
        for i in range(21):
            point = df_frame[df_frame['Landmark'] == i]
            if len(point) == 0:
                continue
            x, y = point.iloc[0][['X', 'Y']]
            dist = np.sqrt((x - 0.5)**2 + (y - 0.5)**2)
            distances.append(dist)
        if distances:
            result.append(np.mean(distances))
    if not result:
        return np.nan
    return np.nanmean(result)

# ---- מעבר על כל הסרטונים ---- #
for idx, row in df.iterrows():
    movie_name = os.path.splitext(row['name of movie'])[0]  # הסרת .mp4
    expected_frames = row['num_frames']
    csv_path = os.path.join(csv_dir, f'{movie_name}.csv')

    if os.path.exists(csv_path):
        try:
            csv_df = pd.read_csv(csv_path)
            unique_frames = csv_df['Frame'].nunique()
            ratio = unique_frames / expected_frames if expected_frames > 0 else 0
            avg_area = compute_area_per_frame(csv_df)
            center_distance = compute_mean_center_distance(csv_df)
            all_x.extend(csv_df['X'].tolist())
            all_y.extend(csv_df['Y'].tolist())

            print(f'✓ {movie_name} | frames: {unique_frames}/{expected_frames:.0f} | ratio: {ratio:.2f} | area: {avg_area:.2f} | center_dist: {center_distance:.3f}')
        except Exception as e:
            print(f'⚠️ Error reading {csv_path}: {e}')
            ratio = None
            avg_area = None
            center_distance = None
    else:
        print(f'⚠️ File not found: {csv_path}')
        ratio = None
        avg_area = None
        center_distance = None

    ratios.append(ratio)
    avg_areas.append(avg_area)
    center_distances.append(center_distance)

# תוספת עמודות ל־DataFrame
df['detected_ratio'] = ratios
df['avg_hand_area'] = avg_areas
df['mean_center_distance'] = center_distances

# חישוב גיל
df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['age'] = (df['date'] - df['birthDate']).dt.days / 365.25

# סינון תינוקות עד גיל שנה
infants = df[df['age'] <= 1].copy()

# גרף: גיל מול מרחק מהמרכז
plt.figure(figsize=(8, 6))
plt.scatter(infants['age'], infants['mean_center_distance'], alpha=0.7, color='darkorange', edgecolor='black')
z = np.polyfit(infants['age'], infants['mean_center_distance'], 1)
p = np.poly1d(z)
plt.plot(infants['age'], p(infants['age']), linestyle='--', color='gray', label='Trend line')

plt.title('Mean Distance from Center vs. Age (Infants under 1 year)', fontsize=14)
plt.xlabel('Age (years)', fontsize=12)
plt.ylabel('Mean Hand Distance from Center (normalized)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# שמירת קובץ אקסל
df.to_excel(output_path, index=False)
print(f'\n✅ קובץ עודכן ונשמר אל: {output_path}')

# --- ציור Heatmap ---
plt.figure(figsize=(7, 6))
sns.kdeplot(x=all_x, y=all_y, fill=True, cmap="plasma", bw_adjust=0.1, levels=100, thresh=0.05)
plt.title('Hand Location Heatmap – All Age Groups', fontsize=14)
plt.xlabel('Normalized X')
plt.ylabel('Normalized Y')
plt.gca().invert_yaxis()  # להפוך את הציר האנכי כך שיהיה כמו בתמונה אמיתית
plt.grid(False)
plt.tight_layout()
plt.show()

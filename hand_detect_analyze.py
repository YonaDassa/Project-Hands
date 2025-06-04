import os
import pandas as pd
import matplotlib.pyplot as plt
"""
This script analyzes hand-detection performance across a series of video files using frame-level CSV data.

Overview of the steps:

1. Reading CSV Files:
   - The script scans a specified folder containing CSV files.
   - Each CSV file corresponds to a single video and contains a list of video frames where hands were detected.
   - For each video, the script counts how many unique frames had hand detections.
   - A summary is created listing each video and the number of detected frames.

2. Saving the Summary:
   - The summarized detection data is saved to a new CSV file called `frames_summary.csv`.
   - This file contains two columns: the video name and the number of frames with detections.

3. Reading the Ground Truth Table:
   - The script reads an additional CSV file (`Fixed_Data_base.csv`) that contains metadata about the videos.
   - This includes the total number of frames per video (`num_frames`), the participant's age (`age`), and the video name (used for merging).

4. Merging the Data:
   - The two data sources (detected and expected) are merged using the video name.
   - This allows for a direct comparison between detected frames and the total number of expected frames.

5. Calculating Detection Ratio:
   - For each video, the detection ratio is calculated as:
     `number of detected frames / total expected frames`

6. Visualization:
   - A scatter plot is generated comparing the expected number of frames with the detected ones.
   - A horizontal line shows the average number of detected frames across all videos.
   - The graph helps assess how well hand detection performed across different videos.

This script is useful for evaluating the effectiveness and coverage of a hand detection algorithm in a video dataset.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Read all CSV files and summarize detected frames
folder_path = r'C:\Users\halle\Documents\data_csv'
summary = []

for filename in os.listdir(folder_path):
    if filename.endswith(".csv") and filename != "frames_summary.csv":
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(file_path, sep=',', encoding='utf-8')

            if len(df.columns) == 1 and ',' in df.columns[0]:
                df.columns = df.columns[0].split(',')

            df.columns = df.columns.str.strip()
            print(f"{filename} columns: {df.columns.tolist()}")

            if 'Frame' in df.columns:
                num_unique_frames = df['Frame'].nunique()
                summary.append({'movie_name': filename.replace('.csv', ''), 'detected_frames': num_unique_frames})
            else:
                print(f"⚠️ 'Frame' column not found in {filename}")
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

# Save the summary
summary_df = pd.DataFrame(summary)
summary_output_file = os.path.join(folder_path, "frames_summary.csv")
summary_df.to_csv(summary_output_file, index=False)
print("✅ Summary saved to:", summary_output_file)

# Step 2: Read summary and expected frames tables, merge by movie name
detected_df = pd.read_csv(summary_output_file)
expected_df = pd.read_csv(r'C:\Users\halle\Documents\Fixed_Data_base.csv')

detected_df.columns = detected_df.columns.str.strip()
expected_df.columns = expected_df.columns.str.strip()

# Merge on movie name
merged = pd.merge(detected_df, expected_df, left_on="movie_name", right_on="name of movie", how='inner')

# Rename columns
merged.rename(columns={'detected_frames': 'detected_frames',
                       'num_frames': 'expected_frames'}, inplace=True)

# Calculate detection ratio
merged["detection_ratio"] = merged["detected_frames"] / merged["expected_frames"]

# === Step 3: Normalize Age ===
merged["age"] = pd.to_numeric(merged["age"], errors='coerce')
merged["detected_frames"] = pd.to_numeric(merged["detected_frames"], errors='coerce')

# Drop missing values
merged = merged.dropna(subset=["age", "detected_frames"])

# --- 1. Z-score Normalization ---
merged["age_zscore"] = (merged["age"] - merged["age"].mean()) / merged["age"].std()

# --- 2. Min-Max Normalization ---
merged["age_minmax"] = (merged["age"] - merged["age"].min()) / (merged["age"].max() - merged["age"].min())

# --- 3. Binning: Group ages into categories ---
bins = [0, 1, 3, 6, 12, 18]
labels = ["<1", "1-3", "3-6", "6-12", "12-18"]
merged["age_group"] = pd.cut(merged["age"], bins=bins, labels=labels, right=False)

# === Visualization 1: Detected vs. Expected Frames ===
plt.figure(figsize=(12, 7))
plt.scatter(merged["expected_frames"], merged["detected_frames"], color='teal', alpha=0.7, label="Detected Frames")
avg_detected = merged["detected_frames"].mean()
plt.axhline(y=avg_detected, color='purple', linestyle='-.', linewidth=2, label=f"Average Detected Frames = {avg_detected:.1f}")
plt.xlabel("Expected Number of Frames")
plt.ylabel("Detected Number of Frames")
plt.title("Detected vs. Expected Frames per Video")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Visualization 2: Age vs. Detected Frames with Trend Line ===
plt.figure(figsize=(12, 7))
plt.scatter(merged["age"], merged["detected_frames"], color='darkblue', alpha=0.7, label="Detected Frames by Age")

# Linear regression
z = np.polyfit(merged["age"], merged["detected_frames"], 1)
p = np.poly1d(z)
plt.plot(merged["age"], p(merged["age"]), "r--", label=f"Trend Line: y = {z[0]:.2f}x + {z[1]:.1f}")

plt.xlabel("Age (in years)")
plt.ylabel("Detected Frames")
plt.title("Detected Hand Frames by Age")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# === Visualization 3: Average Detected Frames per Age Group (Binning) ===
grouped = merged.groupby("age_group")["detected_frames"].mean().reset_index()

plt.figure(figsize=(10, 6))
plt.bar(grouped["age_group"].astype(str), grouped["detected_frames"], color='lightgreen')
plt.xlabel("Age Group (years)")
plt.ylabel("Average Detected Frames")
plt.title("Average Detected Hand Frames by Age Group")
plt.grid(True)
plt.tight_layout()
plt.show()

# קיבוץ לפי גיל (בדיוק) וחישוב ממוצע פריימים לאותו גיל
avg_by_age = merged.groupby('age')['detected_frames'].mean().reset_index()


# גרף קו
plt.figure(figsize=(10, 6))
plt.plot(avg_by_age['age'], avg_by_age['detected_frames'], marker='o', linestyle='-', color='green')
plt.xlabel("Age (months)")
plt.ylabel("Average Detected Frames")
plt.title("Average Detected Frames by Exact Age")
plt.grid(True)
plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 6))
plt.hist(merged["age"], bins=20, color='skyblue', edgecolor='black')
plt.xlabel("Age (in years)")
plt.ylabel("Number of Videos")
plt.title("Distribution of Ages in Dataset")
plt.grid(True)
plt.tight_layout()
plt.show()

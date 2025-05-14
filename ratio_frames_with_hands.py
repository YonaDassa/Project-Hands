import pandas as pd
import os
from datetime import timedelta, datetime, time
import matplotlib.pyplot as plt

# Settings
fps = 29.655
excel_path = r'D:\bar-ilan\final_project\Data\Data_base.xlsx'
csv_dir = r'D:\bar-ilan\final_project\Data'
output_path = r'D:\bar-ilan\final_project\Data\Data_base_with_ratios.xlsx'

# Read the Excel file
df = pd.read_excel(excel_path)

# Function to convert time to seconds
def convert_time_to_seconds(time_obj):
    if isinstance(time_obj, timedelta):
        return time_obj.total_seconds()
    elif isinstance(time_obj, datetime):
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    elif isinstance(time_obj, time):
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    return 0

# Convert 'length' column to frame counts
df['num_frames'] = df['length'].apply(convert_time_to_seconds) * fps

# List to store ratios
ratios = []

# Loop over each row
for idx, row in df.iterrows():
    movie_name = row['name of movie']
    expected_frames = row['num_frames']

    csv_path = os.path.join(csv_dir, f'{movie_name}.csv')

    if os.path.exists(csv_path):
        try:
            csv_df = pd.read_csv(csv_path)
            unique_frames = csv_df['Frame'].nunique()
            ratio = unique_frames / expected_frames if expected_frames > 0 else 0
        except Exception as e:
            print(f'⚠️ Error reading {csv_path}: {e}')
            ratio = None
    else:
        print(f'⚠️ File not found: {csv_path}')
        ratio = None

    ratios.append(ratio)

# Add ratio column
df['detected_ratio'] = ratios

# Convert birth and session dates
df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Calculate age
df['age'] = (df['date'] - df['birthDate']).dt.days / 365.25

# Sort by age
df_sorted = df.sort_values('age')
total_children = len(df_sorted)
group_size = total_children // 3

# Divide into 3 equal age groups
group_1 = df_sorted.iloc[:group_size]
group_2 = df_sorted.iloc[group_size:group_size*2]
group_3 = df_sorted.iloc[group_size*2:]

# Age ranges
age_group_1_range = (group_1['age'].min(), group_1['age'].max())
age_group_2_range = (group_2['age'].min(), group_2['age'].max())
age_group_3_range = (group_3['age'].min(), group_3['age'].max())

# Average ratios
group_1_avg_ratio = group_1['detected_ratio'].mean()
group_2_avg_ratio = group_2['detected_ratio'].mean()
group_3_avg_ratio = group_3['detected_ratio'].mean()

# Print summary
print(f'Group 1: age {age_group_1_range[0]:.2f}-{age_group_1_range[1]:.2f}, average ratio: {group_1_avg_ratio:.2f}')
print(f'Group 2: age {age_group_2_range[0]:.2f}-{age_group_2_range[1]:.2f}, average ratio: {group_2_avg_ratio:.2f}')
print(f'Group 3: age {age_group_3_range[0]:.2f}-{age_group_3_range[1]:.2f}, average ratio: {group_3_avg_ratio:.2f}')

# Save the updated Excel file
df.to_excel(output_path, index=False)
print(f'✅ File successfully saved to: {output_path}')

# Plotting
labels = [
    f'{age_group_1_range[0]:.2f}-{age_group_1_range[1]:.2f} years',
    f'{age_group_2_range[0]:.2f}-{age_group_2_range[1]:.2f} years',
    f'{age_group_3_range[0]:.2f}-{age_group_3_range[1]:.2f} years'
]
avg_ratios = [group_1_avg_ratio, group_2_avg_ratio, group_3_avg_ratio]

plt.figure(figsize=(8, 6))
bars = plt.bar(labels, avg_ratios, color=['skyblue', 'lightgreen', 'salmon'])

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', ha='center', va='bottom', fontsize=10)

plt.title('Average Hand Appearance Ratio by Age Group (equal-sized groups)', fontsize=14)
plt.xlabel('Age Range (years)', fontsize=12)
plt.ylabel('Detected Hand Ratio', fontsize=12)
plt.ylim(0, max(avg_ratios) * 1.2)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# Plot age distribution
plt.figure(figsize=(8, 6))
plt.hist(df['age'].dropna(), bins=15, color='mediumslateblue', edgecolor='black')
plt.title('Distribution of Children\'s Ages in Dataset', fontsize=14)
plt.xlabel('Age (years)', fontsize=12)
plt.ylabel('Number of Children', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

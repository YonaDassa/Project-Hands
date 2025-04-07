import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the CSV file
csv_path = '/home/yona/Project/hands_coordinates.csv'
print(f"Reading data from {csv_path}...")
data = pd.read_csv(csv_path)

# Filter data to focus on X and Y coordinates only
heatmap_data = data[['Frame', 'X', 'Y']].dropna()

# Define heatmap size
heatmap_width = 1280  # heatmap width in pixels
heatmap_height = 720  # heatmap height in pixels

# Convert coordinates to pixel units
heatmap_data['X'] = (heatmap_data['X'] * heatmap_width).clip(0, heatmap_width - 1).astype(int)
heatmap_data['Y'] = (heatmap_data['Y'] * heatmap_height).clip(0, heatmap_height - 1).astype(int)

# Define influence radius and scores
radius = 40  # influence radius in pixels
center_score = 1000  # score for exact point
decay_rate = 0.2  # medium decay rate

# Create a single accumulation array instead of one per frame
final_heatmap = np.zeros((heatmap_height, heatmap_width), dtype=np.float32)  # Using float32 instead of float64

# Get unique frames for progress reporting
unique_frames = heatmap_data['Frame'].unique()
total_frames = len(unique_frames)
print(f"Processing {total_frames} unique frames...")

# Process each frame's data
for i, frame in enumerate(unique_frames):
    if i % 100 == 0:  # Show progress every 100 frames
        print(f"Processing frame {i}/{total_frames}...")
    
    # Get data for this frame only
    frame_data = heatmap_data[heatmap_data['Frame'] == frame]
    
    # Process each point in this frame
    for _, row in frame_data.iterrows():
        x, y = row['X'], row['Y']
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                distance = np.sqrt(dx**2 + dy**2)
                if distance <= radius:  # within radius
                    # Score for center point and surrounding points
                    if distance == 0:
                        score = center_score  # high score for center point
                    else:
                        score = center_score * np.exp(-decay_rate * distance)  # medium decay
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < heatmap_width and 0 <= ny < heatmap_height:
                        final_heatmap[ny, nx] += score

print("Creating heatmap visualization...")
# Create heatmap with matplotlib
plt.figure(figsize=(10, 8))
plt.imshow(final_heatmap, cmap='jet', interpolation='nearest')
plt.colorbar(label='Accumulated Score')
plt.title('Accumulated Heatmap of Hand Landmarks (Moderate Decay)')
plt.xlabel('X')
plt.ylabel('Y')
plt.gca().invert_yaxis()  # Invert Y-axis to match image coordinates

# Save the image
output_path = '/home/yona/Project/hand_heatmap.png'
plt.savefig(output_path)
print(f"Heatmap saved to {output_path}")

plt.show()
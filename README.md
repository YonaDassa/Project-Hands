# Hand Movement Analysis Project

## 📋 Overview


## 🔍 Features


## 🛠️ Technical Details

The system identifies 21 landmarks on each hand using MediaPipe's hand tracking technology. Each landmark contributes to heat intensity through an exponential decay function, with highest values at the landmark center and decreasing as distance increases.

Key methodological choices:
- **Influence Radius**: 40 pixels around each coordinate
- **Decay Function**: Exponential decay for smooth transitions
- **Cumulative Mapping**: Aggregates hand positions across all analyzed frames

## 📊 Applications


## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/YonaDassa/Project-Hands.git
cd Project-Hands

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install opencv-python mediapipe numpy matplotlib pandas
```

## 🚀 Usage

### Basic Usage

```bash
# Process video and generate hand coordinate data every third frame
python skeep_frame.py

# Process video and generate hand coordinate data every third frame with area
python skeep_frame_circle.py

# Generate heat map from coordinates
python hot_maps.py

# inaractive graph
python interactive_graph.py

```

## ⚙️ Configuration

Edit the scripts to adjust these parameters:

- `video_path`: Path to your input video
- `radius`: Influence radius around each hand landmark (default: 40 pixels)
- `decay_rate`: Rate at which influence decreases with distance (default: 0.2)
- `center_score`: Maximum influence value at the center point (default: 1000)

## 📈 Output

The system produces:

1. **CSV Data File**: Contains frame numbers and X,Y,Z coordinates for each hand landmark
2. **Processed Video**: Shows the original video with hand landmarks overlaid

## 🔬 Research Applications

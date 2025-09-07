# ✋ Hand Movement Analysis Project

## 📋 Overview
This project analyzes hand movements in videos using **Google MediaPipe**.  
The system tracks 21 anatomical hand landmarks, processes them into spatial representations, and produces heat maps, scatter plots, and statistical metrics to reveal differences in hand usage across age groups.

## 🔍 Features
- 🎯 Real-time hand landmark detection (21 points per hand)  
- 🔥 Heat map generation of hand positions across frames  
- 📊 Interactive scatter plots for spatial exploration  
- 📏 Relative hand area calculation per frame  
- 🧪 Age-group based comparative analysis (children vs. adults)

## 🛠️ Technical Details
The system identifies 21 landmarks on each hand using **MediaPipe's hand tracking technology**.  
Each landmark contributes to heat intensity through an **exponential decay function**, with maximum influence at the landmark center and decreasing smoothly with distance.

**Key methodological choices:**
- **Influence Radius**: 40 pixels around each coordinate  
- **Decay Function**: Exponential decay for smooth transitions  
- **Cumulative Mapping**: Aggregates hand positions across all analyzed frames

## 📊 Applications
- Developmental research: studying visual-motor coordination in infants vs. adults  
- Clinical insights: potential early markers for neurodevelopmental differences  
- Computer vision & HCI: robust hand-tracking pipelines for gesture analysis

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/YonaDassa/Project-Hands.git
cd Project-Hands

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

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

# Interactive scatter plot of hand positions
python interactive_graph.py
```

## ⚙️ Configuration
Edit the script files to adjust parameters:
- `video_path`: Path to input video
- `radius`: Influence radius around each hand landmark (default: 40 pixels)
- `decay_rate`: Rate of exponential decay (default: 0.2)
- `center_score`: Maximum influence value at the center point (default: 1000)

## 📈 Output
The system produces:
- **CSV Data File**: Frame numbers and X, Y, Z coordinates for each hand landmark
- **Processed Video**: Input video with detected hand landmarks overlaid
- **Heat Maps**: Visual representation of cumulative hand positions
- **Interactive Graphs**: Exploration of spatial hand distributions

## 🔬 Research Applications
This project demonstrates how computational tools such as MediaPipe can be used to quantify developmental patterns of hand movement and visual exposure.

It opens avenues for:
- Understanding visual-motor development in early childhood
- Detecting atypical developmental trajectories
- Building clinical assessment tools for motor-visual integration

## 📚 Project Structure
```
Project-Hands/
├── README.md
├── requirements.txt
├── skeep_frame.py          # Basic frame processing
├── skeep_frame_circle.py   # Frame processing with area calculation
├── hot_maps.py             # Heat map generation
├── interactive_graph.py    # Interactive visualization
├── data/                   # Input videos and output CSV files
└── output/                 # Generated heat maps and visualizations
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors
- **יונה דסה** (Yona Dassa)
- **הלל לוי** (Hillel Levi)

**Supervisor:** Prof. Sharon Gilai-Dotan  
**Institution:** School of Optometry and Vision Sciences, Bar-Ilan University

## 📞 Contact
For questions or collaboration inquiries, please reach out through the GitHub repository.

---
*This project is part of ongoing research into visual-motor development patterns across different age groups.*

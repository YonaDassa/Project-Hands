import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- הגדרות --- #
#csv_folder =  r'C:\Users\halle\Documents\csv_adult'
csv_folder = r'C:\Users\halle\Documents\data_csv'
heatmap_width = 1280
heatmap_height = 720


class DataVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Position Analysis")

        # Initialize data cache
        self.data_cache = {
            "adult": None,
            "child": None
        }

        # Initialize rectangle dimensions
        self.rect_x_min = heatmap_width // 3
        self.rect_x_max = (2 * heatmap_width) // 3
        self.rect_y_min = 0
        self.rect_y_max = heatmap_height

        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create control frame
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=5)

        # Create radio buttons
        self.dataset_var = tk.StringVar(value="child")
        self.radio_frame = ttk.Frame(self.control_frame)
        self.radio_frame.pack(side=tk.LEFT, padx=10)

        ttk.Radiobutton(self.radio_frame, text="Child Data", variable=self.dataset_var,
                        value="child", command=self.update_plot).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(self.radio_frame, text="Adult Data", variable=self.dataset_var,
                        value="adult", command=self.update_plot).pack(side=tk.LEFT, padx=10)

        # Create density slider
        self.density_frame = ttk.Frame(self.control_frame)
        self.density_frame.pack(side=tk.RIGHT, padx=10)

        ttk.Label(self.density_frame, text="Point Density:").pack(side=tk.LEFT, padx=5)
        self.density_var = tk.DoubleVar(value=50.0)
        self.density_slider = ttk.Scale(
            self.density_frame,
            from_=1.0,
            to=100.0,
            orient=tk.HORIZONTAL,
            variable=self.density_var,
            command=self.update_plot
        )
        self.density_slider.pack(side=tk.LEFT, padx=5)
        self.density_label = ttk.Label(self.density_frame, text="50%")
        self.density_label.pack(side=tk.LEFT, padx=5)

        # Create plot frame
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Create Y-range slider (vertical) with clear separation and labels
        self.y_slider_frame = ttk.Frame(self.plot_frame)
        self.y_slider_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=10)

        # Y Max (top)
        self.y_max_label = ttk.Label(self.y_slider_frame, text="Y Max")
        self.y_max_label.pack(side=tk.TOP, pady=(0, 2))
        self.y_max_var = tk.DoubleVar(value=heatmap_height)
        self.y_max_slider = ttk.Scale(
            self.y_slider_frame,
            from_=0,
            to=heatmap_height,
            orient=tk.VERTICAL,
            variable=self.y_max_var,
            command=self.update_plot,
            length=200
        )
        self.y_max_slider.pack(side=tk.BOTTOM, pady=(0, 10))

        # Y Min (bottom)
        self.y_min_label = ttk.Label(self.y_slider_frame, text="Y Min")
        self.y_min_label.pack(side=tk.BOTTOM, pady=(2, 0))
        self.y_min_var = tk.DoubleVar(value=0)
        self.y_min_slider = ttk.Scale(
            self.y_slider_frame,
            from_=0,
            to=heatmap_height,
            orient=tk.VERTICAL,
            variable=self.y_min_var,
            command=self.update_plot,
            length=200
        )
        self.y_min_slider.pack(side=tk.TOP, pady=(10, 0))

        # Create X-range slider (horizontal)
        self.x_slider_frame = ttk.Frame(self.plot_frame)
        self.x_slider_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.x_min_var = tk.DoubleVar(value=self.rect_x_min)
        self.x_max_var = tk.DoubleVar(value=self.rect_x_max)

        self.x_min_slider = ttk.Scale(
            self.x_slider_frame,
            from_=0,
            to=heatmap_width,
            orient=tk.HORIZONTAL,
            variable=self.x_min_var,
            command=self.update_plot
        )
        self.x_min_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.x_max_slider = ttk.Scale(
            self.x_slider_frame,
            from_=0,
            to=heatmap_width,
            orient=tk.HORIZONTAL,
            variable=self.x_max_var,
            command=self.update_plot
        )
        self.x_max_slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # Create figure and canvas
        self.fig = plt.Figure(figsize=(12, 9))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initial plot
        self.update_plot()

    def load_data(self):
        dataset = self.dataset_var.get()

        # Check if data is already in cache
        if self.data_cache[dataset] is not None:
            return self.data_cache[dataset]

        # If not in cache, load the data
        csv_folder = r'C:\Users\halle\Documents\csv_adult' if dataset == "adult" else r'C:\Users\halle\Documents\data_csv'

        all_points = []
        for filename in os.listdir(csv_folder):
            if filename.endswith('.csv'):
                path = os.path.join(csv_folder, filename)
                try:
                    df = pd.read_csv(path)
                    df = df[['Frame', 'X', 'Y']].dropna()
                    df['X'] = (df['X'] * heatmap_width).clip(0, heatmap_width - 1)
                    df['Y'] = (df['Y'] * heatmap_height).clip(0, heatmap_height - 1)

                    grouped = df.groupby('Frame')[['X', 'Y']].mean().reset_index()
                    all_points.append(grouped)
                except Exception as e:
                    print(f'⚠️ Error in {filename}: {e}')

        # Store in cache and return
        self.data_cache[dataset] = pd.concat(all_points, ignore_index=True) if all_points else None
        return self.data_cache[dataset]

    def update_plot(self, *args):
        self.fig.clear()
        all_data = self.load_data()

        if all_data is not None:
            # Update density label
            density = self.density_var.get()
            self.density_label.config(text=f"{density:.0f}%")

            # Sample data based on density
            sample_size = int(len(all_data) * (density / 100.0))
            if sample_size < len(all_data):
                sampled_data = all_data.sample(n=sample_size, random_state=42)
            else:
                sampled_data = all_data

            # Get current rectangle dimensions
            rect_x_min = self.x_min_var.get()
            rect_x_max = self.x_max_var.get()
            rect_y_min = self.y_min_var.get()
            rect_y_max = self.y_max_var.get()

            # Ensure min is less than max
            rect_x_min, rect_x_max = min(rect_x_min, rect_x_max), max(rect_x_min, rect_x_max)
            rect_y_min, rect_y_max = min(rect_y_min, rect_y_max), max(rect_y_min, rect_y_max)

            inside_mask = (
                    (sampled_data['X'] >= rect_x_min) & (sampled_data['X'] <= rect_x_max) &
                    (sampled_data['Y'] >= rect_y_min) & (sampled_data['Y'] <= rect_y_max)
            )
            inside_count = inside_mask.sum()
            outside_count = len(sampled_data) - inside_count

            actual_ratio = inside_count / len(sampled_data) if len(sampled_data) > 0 else np.nan
            expected_ratio = ((rect_x_max - rect_x_min) * (rect_y_max - rect_y_min)) / (heatmap_width * heatmap_height)

            ax = self.fig.add_subplot(111)
            ax.scatter(sampled_data.loc[inside_mask, 'X'], sampled_data.loc[inside_mask, 'Y'],
                       color='blue', alpha=0.4, label='Inside Rectangle')
            ax.scatter(sampled_data.loc[~inside_mask, 'X'], sampled_data.loc[~inside_mask, 'Y'],
                       color='orange', alpha=0.4, label='Outside Rectangle')

            ax.add_patch(plt.Rectangle(
                (rect_x_min, rect_y_min),
                rect_x_max - rect_x_min,
                rect_y_max - rect_y_min,
                edgecolor='red', facecolor='none', linewidth=2, label='Analysis Area'
            ))

            ax.set_title(f'Mean Hand Positions – {self.dataset_var.get().capitalize()} Data', fontsize=16)
            ax.set_xlabel('X (pixels)', fontsize=12)
            ax.set_ylabel('Y (pixels)', fontsize=12)
            ax.set_xlim(0, heatmap_width)
            ax.set_ylim(heatmap_height + 50, -50)
            ax.grid(True, linestyle='--', alpha=0.3)
            ax.legend(loc='upper left', fontsize=10)

            info_text = (
                f'Inside Rectangle: {inside_count}\n'
                f'Outside Rectangle: {outside_count}\n'
                f'Actual Ratio: {actual_ratio:.4f}\n'
                f'Expected Ratio: {expected_ratio:.4f}\n'
                f'Points Shown: {len(sampled_data)}\n'
                f'Rectangle: ({rect_x_min:.0f}, {rect_y_min:.0f}) to ({rect_x_max:.0f}, {rect_y_max:.0f})'
            )
            ax.text(0.02, 0.02, info_text,
                    fontsize=10, color='black',
                    bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'),
                    transform=ax.transAxes)

            self.fig.tight_layout()
            self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizer(root)
    root.mainloop()


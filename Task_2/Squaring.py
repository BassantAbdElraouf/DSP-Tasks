import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_and_process_signal():
    file_path = filedialog.askopenfilename(title="Select Signal File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        # Read the signal from the file
        with open(file_path, "r") as file:
            lines = file.readlines()[3:]  # Skip the first 3 lines
            loaded_signals = [line.strip().split() for line in lines]
            indices = [int(item[0]) for item in loaded_signals]
            values = [float(item[1]) for item in loaded_signals]
        
        # Square the loaded signal
        squared_values = np.square(values)
        
        # Plot the original and squared signals
        original_ax.clear()
        squared_ax.clear()
        
        original_ax.plot(indices, values, color='b', label='Original Signal')
        original_ax.set_title('Original Signal Visualization', color='red')
        original_ax.set_xlabel('Indices')
        original_ax.set_ylabel('Values')
        original_ax.legend()

        squared_ax.plot(indices, squared_values, color='g', label='Squared Signal')
        squared_ax.set_title('Squared Signal Visualization', color='red')
        squared_ax.set_xlabel('Indices')
        squared_ax.set_ylabel('Squared Values')
        squared_ax.legend()

        canvas.draw()

# Create a tkinter window
root = tk.Tk()
root.title("Signal Loader and Squaring")

# Frame for load button
load_frame = tk.Frame(root)
load_frame.pack(pady=10)

# Add a button to load and process the signal
load_button = tk.Button(root, text="Load and Process Signal", font=("Helvetica", 15), bg="blue", fg="white", command=load_and_process_signal)
load_button.pack()

# Create Matplotlib figure and Tkinter canvas to embed the figure in the Tkinter window
fig, (original_ax, squared_ax) = plt.subplots(1, 2, figsize=(12, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(padx=10, pady=10)

root.mainloop()

import tkinter as tk
from tkinter import filedialog, ttk
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
        
        # Normalize the signal based on the selected radio button
        normalization_type = normalization_var.get()
        normalized_values = normalize_signal(values, normalization_type)
        
        # Plot the original and normalized signals
        original_ax.clear()
        normalized_ax.clear()
        
        original_ax.plot(indices, values, color='b', label='Original Signal')
        original_ax.set_title('Original Signal Visualization',color='red')
        original_ax.set_xlabel('Indices')
        original_ax.set_ylabel('Values')
        original_ax.legend()

        normalized_ax.plot(indices, normalized_values, color='g', label='Normalized Signal')
        normalized_ax.set_title('Normalized Signal Visualization',color='red')
        normalized_ax.set_xlabel('Indices')
        normalized_ax.set_ylabel('Normalized Values')
        normalized_ax.legend()

        canvas.draw()

# Function to normalize the signal
def normalize_signal(values, normalization_type):
    if normalization_type == 0:
        # Normalize to the range [0, 1]
        min_value = min(values)
        max_value = max(values)
        normalized_values = np.interp(values, (min_value, max_value), (0, 1))
    else:
        # Normalize to the range [-1, 1]
        min_value = min(values)
        max_value = max(values)
        normalized_values = np.interp(values, (min_value, max_value), (-1, 1))
    return normalized_values

# Create a tkinter window
root = tk.Tk()
root.title("Signal Loader and Normalizer")

# Label above radio buttons
label = tk.Label(root, text="Select Normalization Type", font=("Helvetica", 16))
label.pack(pady=10)

# Frame for radio buttons
radio_frame = tk.Frame(root)
radio_frame.pack(pady=10)

# Configure the font size for Radiobutton text
style = ttk.Style()
style.configure('TRadiobutton', font=('Helvetica', 14))  # Set the font size for Radiobutton text

# Add radio buttons for normalization choices
normalization_var = tk.IntVar()
normalization_var.set(0)  # Default choice: [0, 1] normalization

radio_button_1 = ttk.Radiobutton(radio_frame, text="Normalize to [0, 1]", variable=normalization_var, value=0)
radio_button_2 = ttk.Radiobutton(radio_frame, text="Normalize to [-1, 1]", variable=normalization_var, value=1)
radio_button_1.pack(side='left', padx=10)
radio_button_2.pack(side='left', padx=10)

# Frame for load button
load_frame = tk.Frame(root)
load_frame.pack(pady=10)

# Add a button to load and process the signal
load_button = tk.Button(root, text="Load and Process Signal", font=("Helvetica", 15), bg="blue", fg="white", command=load_and_process_signal)
load_button.pack()

# Create Matplotlib figure and Tkinter canvas to embed the figure in the Tkinter window
fig, (original_ax, normalized_ax) = plt.subplots(1, 2, figsize=(12, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(padx=10, pady=10)

root.mainloop()

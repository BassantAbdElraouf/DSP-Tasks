import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Function to load and process the signal file
def load_and_process_signal():
    # Get the shift value from the entry field
    try:
        shift_value = int(shift_entry.get())
    except ValueError:
        # Clear the existing plots if there's an invalid shift value
        original_ax.clear()
        shifted_ax.clear()
        # Redraw the canvases to remove previous plots
        original_canvas.draw()
        shifted_canvas.draw()
        # Update the error message
        result_label.config(text="Invalid shift value!", fg="red")
        return
    
    file_path = filedialog.askopenfilename(title="Select Signal File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        # Read the signal from the file
        with open(file_path, "r") as file:
            lines = file.readlines()[3:]  # Skip the first 3 lines
            signal = [line.strip().split() for line in lines]
            indices = [int(item[0]) for item in signal]
            values = [float(item[1]) for item in signal]

        # Shift the specified indices
        shifted_signals = [index - shift_value for index in indices]

        # Clear the existing plots
        original_ax.clear()
        shifted_ax.clear()

        # Plot the original signal
        original_ax.plot(indices, values, color='blue', label='Original Signal')
        original_ax.set_title('Original Signal Visualization',color='red')
        original_ax.set_xlabel(' Indices')
        original_ax.set_ylabel(' Values')
        original_ax.legend()

        # Plot the shifted signal
        shifted_ax.plot(shifted_signals, values, color='green', label='Shifted Signal')
        shifted_ax.set_title('Shifted Signal Visualization',color='red')
        shifted_ax.set_xlabel('Shifted Indices')
        shifted_ax.set_ylabel(' Values')
        shifted_ax.legend()

        # Redraw the canvases
        original_canvas.draw()
        shifted_canvas.draw()

        # Clear the error message
        result_label.config(text="", fg="black")

# Create GUI window
root = tk.Tk()
root.title("Signal Shifting")

# Label and entry for shift value
shift_label = tk.Label(root, text="Shift Value:", font=("Helvetica", 14))
shift_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
shift_entry = tk.Entry(root, font=("Helvetica", 12))
shift_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Label to display error messages
result_label = tk.Label(root, text="", fg="red", font=("Helvetica", 12))
result_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

# Create and pack a button to load and process the signal
load_button = tk.Button(root, text="Load and Process Signal", font=("Helvetica", 14), bg="blue", fg="white", command=load_and_process_signal)
load_button.grid(row=2, column=0, columnspan=2, pady=20)

# Create Matplotlib figures and Tkinter canvases to embed the figures in the Tkinter window
original_fig, original_ax = plt.subplots(figsize=(6, 4))
shifted_fig, shifted_ax = plt.subplots(figsize=(6, 4))
original_canvas = FigureCanvasTkAgg(original_fig, master=root)
original_canvas.get_tk_widget().grid(row=3, column=0, padx=10, pady=10)
shifted_canvas = FigureCanvasTkAgg(shifted_fig, master=root)
shifted_canvas.get_tk_widget().grid(row=3, column=1, padx=10, pady=10)

# Run the GUI main loop
root.mainloop()





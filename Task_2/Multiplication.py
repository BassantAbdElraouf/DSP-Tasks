import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Function to load and process the signal file
def load_and_process_signal():
    # Get the constant (multiply factor) from the entry field
    try:
        multiply_factor  = float(constant_entry.get())
    except ValueError:
        # Update the error message for invalid constant
        result_label.config(text="Invalid constant!", fg="red")
        return
    
    file_path = filedialog.askopenfilename(title="Select Signal File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        # Read the signal from the file
        with open(file_path, "r") as file:
            lines = file.readlines()[3:]  # Skip the first 3 lines
            signal = [line.strip().split() for line in lines]
            indices = [int(item[0]) for item in signal]
            values = [float(item[1]) for item in signal]

        # Check if the constant is -1 (to invert the signal)
        if multiply_factor  == -1:
            inverted_signal = [-value for value in values]
        else:
            # Multiply the selected signal by the entered constant
            multiplied_signal = [value * multiply_factor  for value in values]

        # Clear the existing plots
        original_ax.clear()
        processed_ax.clear()

        # Plot the original signal
        original_ax.plot(indices, values, color='blue', label='Original Signal')
        original_ax.set_title('Original Signal Visualization', color='red')
        original_ax.set_xlabel('Indices')
        original_ax.set_ylabel('Values')
        original_ax.legend()

        if multiply_factor  == -1:
            # Plot the inverted signal
            processed_ax.plot(indices, inverted_signal, color='green', label='Inverted Signal')
            processed_ax.set_title('Inverted Signal Visualization', color='red')
        else:
            # Plot the multiplied signal
            processed_ax.plot(indices, multiplied_signal, color='green', label=f'Multiplied Signal ({multiply_factor})')
            processed_ax.set_title(f'Multiplied Signal Visualization', color='red')

        processed_ax.set_xlabel('Indices')
        processed_ax.set_ylabel('Values')
        processed_ax.legend()

        # Redraw the canvases
        original_canvas.draw()
        processed_canvas.draw()

        # Clear the error message
        result_label.config(text="", fg="black")

# Create GUI window
root = tk.Tk()
root.title("Signal Processing")

# Label and entry for constant
constant_label = tk.Label(root, text="Multiply Factor:", font=("Helvetica", 14))
constant_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
constant_entry = tk.Entry(root, font=("Helvetica", 12))
constant_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Label to display error messages
result_label = tk.Label(root, text="", fg="red", font=("Helvetica", 12))
result_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

# Create and pack a button to load and process the signal
load_button = tk.Button(root, text="Load and Process Signal", font=("Helvetica", 14), bg="blue", fg="white", command=load_and_process_signal)
load_button.grid(row=2, column=0, columnspan=2, pady=20)

# Create Matplotlib figures and Tkinter canvases to embed the figures in the Tkinter window
original_fig, original_ax = plt.subplots(figsize=(6, 4))
processed_fig, processed_ax = plt.subplots(figsize=(6, 4))
original_canvas = FigureCanvasTkAgg(original_fig, master=root)
original_canvas.get_tk_widget().grid(row=3, column=0, padx=10, pady=10)
processed_canvas = FigureCanvasTkAgg(processed_fig, master=root)
processed_canvas.get_tk_widget().grid(row=3, column=1, padx=10, pady=10)

# Run the GUI main loop
root.mainloop()

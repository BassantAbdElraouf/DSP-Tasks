import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to accumulate signals from a file (skipping the first 3 lines)
def accumulate_signals_from_file():
    file_path = filedialog.askopenfilename(title="Select Signal File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        try:
            # Read the file and skip the first 3 lines
            with open(file_path, 'r') as file:
                lines = file.readlines()[3:]
                # Extract signals from the lines and convert them to integers
                signals = [line.strip().split() for line in lines]
                indices = [int(item[0]) for item in signals]
                values = [float(item[1]) for item in signals]

            # Check if there are signals to accumulate
            if signals:
                # Convert signals to numpy arrays for easy accumulation
                x = np.array(indices)
                y = np.array(values)
                accumulated_signal = np.cumsum(y, axis=0)

                # Clear the previous plots
                original_ax.clear()
                accumulated_ax.clear()

                # Plot the original signal
                original_ax.plot(x, y, color='b', label='Original Signal')
                original_ax.set_title('Original Signal Visualization',color='red')
                original_ax.set_xlabel('Indices')
                original_ax.set_ylabel('Value')
                original_ax.legend()

                # Plot the accumulated signal
                accumulated_ax.plot(x, accumulated_signal, color='g', label='Accumulated Signal')
                accumulated_ax.set_title('Accumulated Signal Visualization',color='red')
                accumulated_ax.set_xlabel('Indices')
                accumulated_ax.set_ylabel('Accumulated Value')
                accumulated_ax.legend()

                canvas.draw()

                # Update the status label
                result_label.config(text="Signal accumulation successful.", fg="green")

            else:
                result_label.config(text="No signals to accumulate.", fg="red")

        except Exception as e:
            result_label.config(text=f"Error: {str(e)}", fg="red")

# Create GUI window
root = tk.Tk()
root.title("Signal Accumulation")

# Create and pack a button to load and accumulate signals
load_button = tk.Button(root, text="Load and Accumulate Signals", font=("Helvetica", 14),
                        bg="blue", fg="white", command=accumulate_signals_from_file)
load_button.pack(pady=20)

# Create Matplotlib figures and Tkinter canvas to embed the figures in the Tkinter window
fig, (original_ax, accumulated_ax) = plt.subplots(1, 2, figsize=(12, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(padx=10, pady=10)

# Label to display status messages
result_label = tk.Label(root, text="", fg="black", font=("Helvetica", 12))
result_label.pack(pady=10)

# Run the GUI main loop
root.mainloop()

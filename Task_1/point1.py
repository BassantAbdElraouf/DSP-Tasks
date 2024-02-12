import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Signal Visualization")

# Specify the number of rows to skip
rows_to_skip = 3

# Read data from the file
with open('signal1.txt', 'r') as file:
    # Skip specified number of rows
    for _ in range(rows_to_skip):
        next(file)

    # Read the remaining lines and split them into indices and values
    data = [line.strip().split() for line in file]

# Extract indices and samples from data
indices, samples = zip(*[(int(line[0]), float(line[1])) for line in data])
# Create a figure and subplots
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,6))

# Plot continuous representation
ax[0].set_title('Continuous Signal Visualization',color='red')
ax[0].plot(indices, samples, marker='o', markersize=5, color='b', label='Continuous')
ax[0].set_xlabel('Indices')
ax[0].set_ylabel('Samples')
# Plot discrete representation
ax[1].set_title('Discrete Signal Visualization',color='red')
ax[1].stem(indices, samples, linefmt='b', markerfmt='b', label='Discrete')
ax[1].set_xlabel('Indices')
ax[1].set_ylabel('Samples')
ax[0].legend()
ax[1].legend()

# Create Tkinter window and canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add a label
label = tk.Label(root, text="Signal Visualization", font=("Helvetica", 20),foreground="blue")
label.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()

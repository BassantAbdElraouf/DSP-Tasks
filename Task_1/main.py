import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import filedialog
from comparesignals import SignalSamplesAreEqual

def generate_signal():
    amplitude = float(e2.get())
    analog_frequency = float(e3.get())
    sampling_frequency = int(e4.get())
    phase_shift_theta = float(e5.get())
    samples = np.arange(0, 1, 1 / sampling_frequency)

    if signal_type.get() == "Sine":
        indices = amplitude * np.sin(2 * np.pi * analog_frequency * samples + phase_shift_theta)
        # Testing Sin_output
        SignalSamplesAreEqual('Task_1/Outputs/SinOutput.txt', samples, indices)
    else:
        indices = amplitude * np.cos(2 * np.pi * analog_frequency * samples + phase_shift_theta)
        # Testing Cos_output
        SignalSamplesAreEqual('Task_1/Outputs/CosOutput.txt', samples, indices)

    # Clear previous plots
    for a in ax[:2]:
        a.clear()

    # Plot continuous representation
    ax[0].set_title('Continuous Signal Visualization', color='red')
    ax[0].plot(samples, indices, marker='o', markersize=5, color='b', label='Continuous')
    ax[0].set_xlabel('Indices')
    ax[0].set_ylabel('Samples')
    # Plot discrete representation
    ax[1].set_title('Discrete Signal Visualization', color='red')
    ax[1].stem(samples, indices, linefmt='b', markerfmt='b', label='Discrete')
    ax[1].set_xlabel('Indices')
    ax[1].set_ylabel('Samples')

    canvas.draw()

def load_signal():
    file_path = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])

    if file_path:
        # Read data from the file, skipping the first 3 rows
        with open(file_path, 'r') as file:
            for _ in range(3):
                next(file)  # Skip the first 3 rows

            data = [line.strip().split() for line in file]

        # Check if each line has at least two elements
        valid_data = [line for line in data if len(line) >= 2]

        if not valid_data:
            print("Error: Invalid data format in the file.")
            return

        # Extract indices and samples from data
        indices, samples = zip(*[(int(line[0]), float(line[1])) for line in valid_data])

        # Clear previous plots
        for a in ax[:2]:
            a.clear()

        # Plot continuous representation
        ax[0].set_title('Continuous Signal Visualization', color='red')
        ax[0].plot(indices, samples, marker='o', markersize=5, color='b', label='Continuous')
        ax[0].set_xlabel('Indices')
        ax[0].set_ylabel('Samples')
        # Plot discrete representation
        ax[1].set_title('Discrete Signal Visualization', color='red')
        ax[1].stem(indices, samples, linefmt='b', markerfmt='b', label='Discrete')
        ax[1].set_xlabel('Indices')
        ax[1].set_ylabel('Samples')

        # Redraw canvas
        canvas.draw()

t = Tk()
t.title('Signal Visualization')
t.geometry('1200x800')

# GUI
signal_type = StringVar()
signal_type.set("Sine")
Label(t, text="Select Signal Type", font=("Helvetica", 22), foreground="black").grid(row=0, column=0, columnspan=2)
Radiobutton(t, text="Sine Wave", font=("Helvetica", 18), foreground="blue", variable=signal_type, value="Sine").grid(row=1, column=0, columnspan=2)
Radiobutton(t, text="Cosine Wave", font=("Helvetica", 18), foreground="blue", variable=signal_type, value="Cosine").grid(row=2, column=0, columnspan=2)

Label(t, text="Enter The Amplitude:", font=("Helvetica", 18), foreground="black").grid(row=3, column=0, sticky="w")
e2 = Entry(t, width=30)
e2.grid(row=3)
Label(t, text="Enter The Analog Frequency:", font=("Helvetica", 18), foreground="black").grid(row=4, column=0, sticky="w")
e3 = Entry(t, width=30)
e3.grid(row=4)
Label(t, text="Enter The Sampling Frequency:", font=("Helvetica", 18), foreground="black").grid(row=5, column=0, sticky="w")
e4 = Entry(t, width=30)
e4.grid(row=5)
Label(t, text="Enter The Phase Shift:", font=("Helvetica", 18), foreground="black").grid(row=6, column=0, sticky="w")
e5 = Entry(t, width=30)
e5.grid(row=6)

generate_button = Button(t, text="Generate Signal", command=generate_signal, width=20, height=3, bg="blue", fg="white")
generate_button.grid(row=7, column=0,  pady=5)

# Load button first point
load_button = Button(t, text="Load Signal", command=load_signal, width=20, height=3, bg="green", fg="white")
load_button.grid(row=8, column=0,  pady=5)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
canvas = FigureCanvasTkAgg(fig, master=t)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=9, column=0, columnspan=2, pady=6)

t.columnconfigure(0, weight=1)
t.rowconfigure(9, weight=1)

t.mainloop()

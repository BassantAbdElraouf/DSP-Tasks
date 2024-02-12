import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from tkinter import *
from comparesignal2 import SignalSamplesAreEqual

def dct(input_signal):
    N = len(input_signal)
    dct_result = [0] * N

    for k in range(N):
        sum_value = 0
        for n in range(N):
            sum_value += input_signal[n] * math.cos((math.pi / (4*N)) * ((2 * n) - 1) *((2*k)-1))

        alpha = math.sqrt(2/N)
        dct_result[k] = alpha * sum_value

    return dct_result

def save_coefficients_to_file(coefficients, filename):
    with open(filename, 'w') as file:
        for k, coef in enumerate(coefficients):
            file.write(f"{k} {coef:.6f}\n")

def remove_dc_component(input_signal):
    mean_value = np.mean(input_signal)
    return input_signal - mean_value

def format_output(signal_values):
    formatted_values = [f"{i} {value:.3f}" for i, value in enumerate(signal_values)]
    return formatted_values

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        data = np.loadtxt(file, delimiter=' ')
        time_values = data[:, 0]
        signal_values = data[:, 1]
        return time_values, signal_values

def plot_signals(input_signal, output_signal, ax1, ax2):
    ax1.clear()
    ax1.set_title('Input Signal Visualization', color='red')
    ax1.plot(input_signal, marker='o', markersize=5, color='b', label='Input')
    ax1.set_xlabel('Indices')
    ax1.set_ylabel('Samples')

    ax2.clear()
    ax2.set_title('DCT Coefficients Visualization', color='red')
    ax2.plot(output_signal, marker='o', markersize=5, color='g', label='DCT')
    ax2.set_xlabel('Indices')
    ax2.set_ylabel('Samples')

    ax1.figure.canvas.draw()
    ax2.figure.canvas.draw()

root = Tk()
root.title("DCT Application")

figure1, ax1 = plt.subplots(figsize=(6, 7))
canvas1 = FigureCanvasTkAgg(figure1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.pack(side=LEFT)

figure2, ax2 = plt.subplots(figsize=(6, 7))
canvas2 = FigureCanvasTkAgg(figure2, master=root)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.pack(side=RIGHT)

def load_and_plot_signal():
    global dct_result
    file_path = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])

    if file_path:
        time_values, signal_values = read_input_file(file_path)

        # Remove DC component
        signal_values_no_dc = remove_dc_component(signal_values)

        # Run DCT
        dct_result = dct(signal_values)

        #Testing DCT
        SignalSamplesAreEqual('Task_5/OutputSignals/DCT_output.txt', dct_result)

        # Plot input and DCT signals
        plot_signals(signal_values_no_dc, dct_result, ax1, ax2)

        # Enable the entry for 'm'
        m_entry.config(state='normal')

load_plot_button = Button(root, text="Apply DCT", command=load_and_plot_signal, width=15, height=2, bg="blue", fg="white")
load_plot_button.pack(pady=10)

m_entry = Entry(root, state='disabled')
m_entry.pack(pady=5)

def save_coefficients():
    m = int(m_entry.get())
    if m > 0 and m <= len(dct_result):
        save_coefficients_to_file(dct_result[:m], 'Task_5/OutputSignals/Saved_coefficients.txt')
        print(f"The first {m} DCT coefficients have been saved to 'dct_coefficients.txt'.")
    else:
        print("Invalid value of 'm'. Please enter a valid value.")

save_button = Button(root, text="Save Coefficients", command=save_coefficients, width=17, height=2, bg="blue", fg="white")
save_button.pack(pady=10)

def remove_dc_and_plot_signal():
    file_path = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])

    if file_path:
        time_values, signal_values = read_input_file(file_path)

        # Remove DC component
        signal_values_no_dc = remove_dc_component(signal_values)

        # Display the original and modified signals
        plot_signals(signal_values, signal_values_no_dc, ax1, ax2)

        # Testing DC removal
        SignalSamplesAreEqual('Task_5/OutputSignals/DC_component_output.txt', signal_values_no_dc)

remove_dc_button = Button(root, text="Remove DC", command=remove_dc_and_plot_signal, width=15, height=2, bg="red", fg="white")
remove_dc_button.pack(pady=10)

root.mainloop()

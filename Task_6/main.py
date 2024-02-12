import tkinter as tk
from tkinter import filedialog
import numpy as np
from Shift_Fold_Signal import Shift_Fold_Signal
from comparesignals import SignalSamplesAreEqual
from ConvTest import ConvTest
from comparesignal2 import SignalSamplesAreEqual
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

indices_values = None
signal_values = None
folded_indices = None
folded_signal = None

def read_input_file(file_path):
    global indices_values, signal_values
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)
        data = np.genfromtxt(file, delimiter=' ', filling_values=np.nan)
        data = data[~np.isnan(data[:, 1])]
        indices_values = data[:, 0]
        signal_values = data[:, 1]
        return indices_values, signal_values

def moving_average(data, window_size):
    weights = np.ones(window_size) / window_size
    return np.convolve(data, weights, mode='valid')

def smoothing(file_path, window_size):
    indices_values, signal_values = read_input_file(file_path)
    smoothed_signal = moving_average(signal_values, window_size)
    plot_signals_in_gui(indices_values, signal_values, indices_values[window_size - 1:], smoothed_signal,
                        title1="Original Signal", title2="Smoothed Signal")
    
    #Testing Smoothing
    SignalSamplesAreEqual(file_path, signal_values)

def run_smoothing(window_size_entry, file_path):
    window_size = int(window_size_entry.get())
    indices_values, signal_values = read_input_file(file_path)
    smoothing(file_path, window_size)

def DerivativeSignal():
    InputSignal = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0,
                   19.0, 20.0, 21.0, 22.0,23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0,
                   36.0, 37.0, 38.0, 39.0,40.0, 41.0, 42.0,43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0,
                   53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0,63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0,
                   70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0,83.0, 84.0, 85.0, 86.0,
                   87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0,100.0]

    expectedOutput_first = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                            1, 1, 1, 1, 1, 1]
    expectedOutput_second = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Compute first derivative
    FirstDrev = [InputSignal[0]]  
    for i in range(1, len(InputSignal)-1):
        FirstDrev.append(InputSignal[i] - InputSignal[i - 1])

    # Compute second derivative
    SecondDrev = [0]  
    for i in range(1, len(FirstDrev)):
        SecondDrev.append(FirstDrev[i] - FirstDrev[i - 1])

    #Testing Sharpening
    if( (len(FirstDrev)!=len(expectedOutput_first)) or (len(SecondDrev)!=len(expectedOutput_second))):
        print("mismatch in length") 
        return
    first=second=True
    for i in range(len(expectedOutput_first)):
        if abs(FirstDrev[i] - expectedOutput_first[i]) < 0.01:
            continue
        else:
            first=False
            print("1st derivative wrong")
            return
    for i in range(len(expectedOutput_second)):
        if abs(SecondDrev[i] - expectedOutput_second[i]) < 0.01:
            continue
        else:
            second=False
            print("2nd derivative wrong") 
            return
    if(first and second):
        print("Derivative Test case passed successfully")
    else:
        print("Derivative Test case failed")
    return

def delay_advance_signal(k_entry):
    global indices_values
    indices_values = np.array([-2, -1, 0, 1, 2, 3, 4, 5, 6])
    signal_values = np.array([1, 1, -1, 0, 0, 3, 3, 2, 1])
    k = int(k_entry.get())
    delayed_indices = indices_values + k

    #Testing Delay Or Advance Signal
    ConvTest(indices_values, signal_values)

    plot_signals_in_gui(indices_values, signal_values, delayed_indices, signal_values, title1="Original Signal",
                        title2="Delayed/Advanced Signal")

def fold_signal():
    global indices_values, signal_values
    file_path = open_file()
    indices_values, signal_values = read_input_file(file_path)
    folded_signal = signal_values[::-1]

    #Testing Folding
    SignalSamplesAreEqual(file_path, signal_values)

    plot_signals_in_gui(indices_values, signal_values, indices_values[::-1], signal_values[::-1],
                        title1="Original Signal", title2="Folded Signal")

def fold(indices_values, signal_values):
    folded_signal = signal_values[::-1]  # Reverse the signal
    return indices_values, folded_signal

def delay(indices_values, k):
    delayed_indices = indices_values + k
    return delayed_indices

def delay_folded_signal(k_entry, folded_indices, signal_values):
    file_path = open_file()
    indices_values, signal_values = read_input_file(file_path)
    k = int(k_entry.get())
    folded_indices, folded_signal = fold(indices_values, signal_values)
    delayed_indices = delay(folded_indices, k)
    if k == 500:
        Shift_Fold_Signal('Task_6/Outputs/Output_ShifFoldedby500.txt',delayed_indices,folded_signal)
    elif k == -500:
        Shift_Fold_Signal('Task_6/Outputs/Output_ShiftFoldedby-500.txt',delayed_indices,folded_signal)

    plot_signals_in_gui(folded_indices, folded_signal, delayed_indices, folded_signal,
                        title1="Folded Signal", title2="Delayed/Advanced Folded Signal")

def DFT(signal):
    n = len(signal)
    amplitude = np.zeros(n)
    frequencies = np.zeros(n)
    phase = np.zeros(n)

    for i in range(n):
        sum_real = 0.0
        sum_imag = 0.0

        for t in range(n):
            angle = -2 * np.pi * i * t / n
            sum_real += signal[t] * np.cos(angle)
            sum_imag += signal[t] * np.sin(angle)

        amplitude[i] = np.sqrt(sum_real**2 + sum_imag**2)
        phase[i] = np.arctan2(sum_imag, sum_real)

    return amplitude, phase

def IDFT(samples, phases):
    n = len(samples)
    s = np.zeros(n, dtype=complex)
    for i in range(n):
        x = 1j * samples[i] * np.sin(phases[i])
        y = samples[i] * np.cos(phases[i])
        s[i] = x + y

    s[0] = 0
    signal = np.zeros(n, dtype=complex)
    for i in range(n):
        for k in range(n):
            val = s[k] * np.exp((2j * np.pi * i * k) / n)
            signal[i] += val

    res = signal.real / n
    return res

def remove_dc_component_using_dft(signal):
    amplitude, phase = DFT(signal)
    amplitude[0] = 0
    phase[0] = 0

    # Run IDFT
    signal_no_dc = IDFT(amplitude, phase)

    # Testing DC removal
    SignalSamplesAreEqual('Task_6/Outputs/DC_component_output.txt', signal_no_dc)

    plot_signals_in_gui(range(len(signal)), signal, range(len(signal)),signal_no_dc, 
                        title1="Original Signal", title2="Signal without DC Component")
    
    return signal_no_dc

def format_output(signal_values):
    formatted_values = [f"{i} {value:.3f}" for i, value in enumerate(signal_values)]
    return formatted_values

def run_removedc():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    time_values, signal_values = read_input_file(file_path)
    signal_values_no_dc = remove_dc_component_using_dft(signal_values)
    signal_values = format_output(signal_values)
    formatted_values = format_output(signal_values_no_dc)

    indices, float_values = zip(*(map(float, value.split()) for value in formatted_values))
    formatted_values_np = np.array(float_values)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    return file_path

# GUI
root = tk.Tk()
root.title("Signal Processing")

frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, padx=10, pady=10)

window_size_label = tk.Label(frame1, text="Enter Window Size:")
window_size_entry = tk.Entry(frame1)
smoothing_button = tk.Button(frame1, text="Run Smoothing", command=lambda: run_smoothing(window_size_entry, open_file()),
                              width=15, height=2, bg="blue", fg="white")

window_size_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
window_size_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
smoothing_button.grid(row=1, column=0, columnspan=2, pady=5)

frame2 = tk.Frame(root)
frame2.grid(row=0, column=1, padx=10, pady=10)

sharpening_button = tk.Button(frame2,text="Run Sharpening", command=DerivativeSignal,width=15, height=2, bg="blue", fg="white")
sharpening_button.grid(row=0, column=0, pady=5)

fold_button = tk.Button(frame2, text="Fold Signal", command=fold_signal, width=15, height=2, bg="blue", fg="white")
fold_button.grid(row=1, column=0, columnspan=2, pady=5)

frame3 = tk.Frame(root)
frame3.grid(row=0, column=2, padx=10, pady=10)

steps_label = tk.Label(frame3, text="Enter Number of Steps:")
Ksteps_entry = tk.Entry(frame3)
delay_advance_button = tk.Button(frame3, text="Delay Signal", command=lambda: delay_advance_signal(Ksteps_entry),
                                 width=15, height=2, bg="blue", fg="white")

steps_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
Ksteps_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
delay_advance_button.grid(row=1, column=0, columnspan=2, pady=5)

frame4 = tk.Frame(root)
frame4.grid(row=0, column=3, padx=10, pady=10)

delay_label = tk.Label(frame4, text="Enter Delay for Folded Signal:")
Kfolded_steps_entry = tk.Entry(frame4)
delay_folded_button = tk.Button(frame4, text="Delay Folded Signal",
                                command=lambda: delay_folded_signal(Kfolded_steps_entry, folded_indices, signal_values),
                                width=15, height=2, bg="blue", fg="white")

delay_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
Kfolded_steps_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
delay_folded_button.grid(row=2, column=0, columnspan=2, pady=5)

figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
figure_canvas = FigureCanvasTkAgg(figure, master=root)
figure_canvas_widget = figure_canvas.get_tk_widget()
figure_canvas_widget.grid(row=1, column=0, columnspan=4)

frame5 = tk.Frame(root)
frame5.grid(row=2, column=0, columnspan=4, pady=10) 

process_button = tk.Button(frame5, text="Remove DC", command=run_removedc, width=20, height=2, bg="blue", fg="white")
process_button.grid(row=0, column=0, columnspan=2, pady=5)

def plot_signals_in_gui(indices_values1, signal_values1, indices_values2, signal_values2, title1="Signal", title2="Signal", color1='red', color2='blue'):
    ax1.clear()
    ax2.clear()

    ax1.plot(indices_values1, signal_values1, label=title1, color='blue')
    ax1.set_xlabel('Indices')
    ax1.set_ylabel('Samples')
    ax1.set_title(title1, color='red')
    ax1.legend()

    ax2.plot(indices_values2, signal_values2, label=title2, color='green')
    ax2.set_xlabel('Indices')
    ax2.set_ylabel('Samples')
    ax2.set_title(title2, color='red')
    ax2.legend()

    figure_canvas.draw()

plot_signals_in_gui([], [], [], [])
root.mainloop()

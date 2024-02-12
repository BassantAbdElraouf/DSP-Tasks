import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ConvTest import ConvTest
from CompareSignal import Compare_Signals


def DFTConv(signal, sampling_frequency):
    n = len(signal)
    amplitude = np.zeros(n)
    frequencies = np.zeros(n)
    phase = np.zeros(n)
    Ts = 1 / sampling_frequency

    for i in range(n):
        sum_real = 0.0
        sum_imag = 0.0

        for t in range(n):
            angle = -2 * np.pi * i * t / n
            sum_real += signal[t] * np.cos(angle)
            sum_imag += signal[t] * np.sin(angle)

        amplitude[i] = np.sqrt(sum_real**2 + sum_imag**2)
        phase[i] = np.arctan2(sum_imag, sum_real)
        frequencies[i] = i / (n * Ts)

    return frequencies, amplitude, phase

def IDFTConv(samples, phases):
    n = len(samples)
    s = np.zeros(n, dtype=complex)
    for i in range(n):
        x = 1j * samples[i] * np.sin(phases[i])
        y = samples[i] * np.cos(phases[i])
        s[i] = (x + y)
    signal = np.zeros(n, dtype=complex)
    for i in range(n):
        for k in range(n):
            val = s[k] * np.exp((2j * np.pi * i * k) / n)
            signal[i] += val

    res = signal.real / n
    return res

def DFTCorr(signal):
    n = len(signal)
    amplitudes = np.zeros(n)
    phases = np.zeros(n)

    for i in range(n):
        t = np.arange(n)
        real_part = np.sum(signal * np.cos(2 * np.pi * i * t / n))
        imag_part = np.sum(signal * np.sin(2 * np.pi * i * t / n))

        amplitudes[i] = np.sqrt(real_part**2 + imag_part**2) / n  # Apply scaling factor here
        phases[i] = np.arctan2(imag_part, real_part)

    return amplitudes, phases

def IDFTCorr(amplitudes, phases):
    n = len(amplitudes)
    res = np.zeros(n)

    for i in range(n):
        t = np.arange(n)
        res += amplitudes[i] * np.cos(2 * np.pi * i * t / n - phases[i])

    return res

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        data = np.loadtxt(file, delimiter=' ')
        indices = data[:, 0]
        signal = data[:, 1]
        return indices, signal

def fast_convolution(indices1, indices2, signal1, signal2):
    # Append zeros to the signals
    ln = len(signal1) + len(signal2) - 1
    padded_signal1 = np.pad(signal1, (0, ln - len(signal1)))
    padded_signal2 = np.pad(signal2, (0, ln - len(signal2)))

    # Calculate DFT of each signal
    freq1, amplitude1, phase1 = DFTConv(padded_signal1, 3)
    freq2, amplitude2, phase2 = DFTConv(padded_signal2, 3)

    res = np.multiply(amplitude1, amplitude2)
    phase = np.add(phase1, phase2)

    # Perform IDFT on the result
    result = IDFTConv(res, phase)

    result_samples = [round(val) for val in result]
    result_indices = list(range(int(indices1[0] + indices2[0]), int(indices1[-1] + indices2[-1]) + 1))

    # Print result in the specified format
    print("Result of Fast Convolution:")
    print("expected_indices =", result_indices)
    print("expected_samples =", result_samples)

    # Testing
    ConvTest(result_indices, result)

    return result

def fast_correlation(signal1, signal2):
    # Calculate DFT of each signal
    amplitudes1, phases1 = DFTCorr(signal1)
    amplitudes2, phases2 = DFTCorr(signal2)

    # Multiply the magnitudes and subtract the phase differences
    corr_amplitudes = amplitudes1 * amplitudes2
    corr_phases =(phases2 - phases1 + np.pi) % (2 * np.pi) - np.pi

    # Perform IDFT on the result
    result = IDFTCorr(corr_amplitudes, corr_phases)
    
    # Print the formatted result
    print("\n")
    print("Result of Fast Correlation:")
    for i, val in enumerate(result):
        print(f"{i} {val:.1f}")

    return result

# GUI
class SignalProcessingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing GUI")

        self.convolve_button = tk.Button(root, text="Fast Convolution", command=self.load_and_convolve,
                                         font=("Helvetica", 14), bg="blue", fg="white")
        self.convolve_button.pack(pady=5)

        self.correlate_button = tk.Button(root, text="Fast Correlation", command=self.load_and_correlate,
                                          font=("Helvetica", 14), bg="blue", fg="white")
        self.correlate_button.pack(pady=5)

        self.fig, self.ax = plt.subplots(1, 3, figsize=(15, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.loaded_signals = []

    def load_and_convolve(self):
        file_paths = filedialog.askopenfilenames(title="Select convolution input files")

        if len(file_paths) == 2:
            signals = [read_input_file(file_path)[1] for file_path in file_paths]
            indices1, indices2 = [read_input_file(file_path)[0] for file_path in file_paths]

            result_convolution = fast_convolution(indices1, indices2, *signals)

            # Plot signals and result
            self.plot_signals_and_result(indices1, signals[0],indices2, signals[1], result_convolution)

        else:
            print("Please select exactly 2 files.")

    def load_and_correlate(self):
        file_paths = filedialog.askopenfilenames(title="Select correlation input files")

        if len(file_paths) == 2:
            signals = [read_input_file(file_path)[1] for file_path in file_paths]
            indices1, indices2 = [read_input_file(file_path)[0] for file_path in file_paths]

            result_correlation = fast_correlation(*signals)

            # Plot signals and result
            self.plot_signals_and_result(indices1, signals[0],indices2, signals[1], result_correlation)
        
            # Testing
            Compare_Signals('Task_9/Fast Correlation/Corr_Output.txt', indices1 , result_correlation)

        else:
            print("Please select exactly 2 files.")

    def plot_signals_and_result(self, indices1, signal1, indices2, signal2, result):
        for ax in self.ax:
            ax.clear()

        self.ax[0].plot(indices1, signal1, label="Signal 1", color='green')
        self.ax[0].set_xlabel('Indices')
        self.ax[0].set_ylabel('Samples')
        self.ax[0].set_title('Signal 1 Visualization',color='red')

        self.ax[1].plot(indices2, signal2, label="Signal 2", color='orange')
        self.ax[1].set_xlabel('Indices')
        self.ax[1].set_ylabel('Samples')
        self.ax[1].set_title('Signal 2 Visualization',color='red')

        self.ax[2].plot(range(len(result)), result, label="Result", color='blue')
        self.ax[2].set_xlabel('Indices')
        self.ax[2].set_ylabel('Samples')
        self.ax[2].set_title('Convolution/Correlation Result',color='red')

        self.ax[0].legend()
        self.ax[1].legend()
        self.ax[2].legend()

        self.canvas.draw()

root = tk.Tk()
app = SignalProcessingGUI(root)
root.mainloop()

import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)
        
        data = np.loadtxt(file, delimiter=' ')
        time = data[:, 0]
        signal = data[:, 1]
        return time, signal
    
def DFT(signal, sampling_frequency):
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
    
    for a, p, f in zip(amplitude, phase, frequencies):
        formatted_amplitude = int(a) if a.is_integer() else f"{a:.14f}f"
        formatted_phase = int(p) if p.is_integer() else f"{p:.14f}f"
        print(f"{formatted_amplitude} {formatted_phase}")


    return frequencies, amplitude, phase

def read_input_file_IDFT(file_path):
    indices = []
    samples = []
    with open(file_path, 'r') as f:
        for _ in range(3):
            next(f)

        for line in f:
            L = line.strip()
            if ',' in L:
                V1, V2 = map(lambda x: float(x.rstrip('f')), L.split(','))
                indices.append(V1)
                samples.append(V2)
    
    return indices, samples

def IDFT(file):
    samples, phases = read_input_file_IDFT(file)
    n = len(samples)
    s= np.zeros(n, dtype=complex)
    for i in range(n):
        x = 1j * samples[i] * np.sin(phases[i])
        y = samples[i] * np.cos(phases[i])
        s[i] = ( x + y)
    signal = np.zeros(n, dtype=complex)
    for i in range(n):
        for k in range(n):
            val = s[k] * np.exp((2j * np.pi * i * k) / n)
            signal[i] += val

    res = signal.real / n

    print("indices\tValues")
    for i in range(len(res)):
        print(f"{i}\t{round(res[i])}")

    return res


if __name__ == "__main__":
    dft_file_path = "Inputs Signals/input_Signal_DFT.txt"
    idft_file_path = "Inputs Signals/input_Signal_IDFT_A,Phase.txt"
    sampling_frequency = 1000  # Replace with your actual sampling frequency
    time, signal = read_input_file(dft_file_path)
    frequencies, amplitude, phase = DFT(signal, sampling_frequency)
    idft_result = IDFT(idft_file_path)

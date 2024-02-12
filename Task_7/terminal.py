import numpy as np
import tkinter as tk
from tkinter import filedialog
from ConvTest import ConvTest

def readFile(file):
    indices = []
    samples = []
    with open(file, 'r') as f1:
        for _ in range(3):  # Skip the first 3 lines
            next(f1)
        
        for line in f1:
            if not line.strip():
                break
            
            V1, V2 = map(float, line.split())
            indices.append(V1)
            samples.append(V2)

    return np.array(indices), np.array(samples)

def convolve_signals():
    file_path1 = filedialog.askopenfilename(title="Select Signal 1 File")
    file_path2 = filedialog.askopenfilename(title="Select Signal 2 File")

    indices1, samples1 = readFile(file_path1)
    indices2, samples2 = readFile(file_path2)

    len_signal1 = len(samples1)
    len_signal2 = len(samples2)
    len_result = len_signal1 + len_signal2 - 1

    result_samples = [0] * len_result
    result_indices = np.arange(len_result) + min(indices1) + min(indices2)

    for i in range(len_signal1):
        for j in range(len_signal2):
            result_samples[i + j] += samples1[i] * samples2[j]

    print("Convolution result indices:", result_indices)
    print("Convolution result samples:", result_samples)
    ConvTest(result_indices,result_samples)

# Create the main window
window = tk.Tk()
window.title("Signal Convolution")

# Create a button to trigger convolution
convolve_button = tk.Button(window, text="Convolve Signals", command=convolve_signals)
convolve_button.pack(pady=20)

# Run the GUI
window.mainloop()

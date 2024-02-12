import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from CompareSignal import Compare_Signals
import numpy as np
import math

def calculate_correlation(signal1, signal2, float_point):
    N = len(signal1)
    result = []

    x1_square = [i ** 2 for i in signal1]
    x2_square = [i ** 2 for i in signal2]
    p12_denominator = math.sqrt((sum(x1_square) * sum(x2_square))) / N
    p12_denominator = round(p12_denominator, float_point)

    for i in range(1, N + 1):
        signal2_shifted = np.concatenate((signal2[i:], signal2[:i]))  
        r = round(np.sum(signal1 * signal2_shifted) / N, float_point)
        p = round(r / p12_denominator, float_point)
        result.append(p)

    result = [result[N - 1]] + result
    indices = list(range(N))
    return indices, result[:N]

class SignalConvolutionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Signal Correlation")

        self.load_button = tk.Button(self, text="Load and correlate Signals", command=self.Correlate_signals,
                                     font=("Helvetica", 15), bg="blue", fg="white")
        self.load_button.pack(pady=20)

        # GUI
        fig_size = (5, 6)
        self.fig1, self.ax1 = plt.subplots(figsize=fig_size)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self)
        self.canvas_widget1 = self.canvas1.get_tk_widget()
        self.canvas_widget1.pack(side=tk.LEFT)

        self.fig2, self.ax2 = plt.subplots(figsize=fig_size)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self)
        self.canvas_widget2 = self.canvas2.get_tk_widget()
        self.canvas_widget2.pack(side=tk.LEFT)

        self.fig3, self.ax3 = plt.subplots(figsize=fig_size)
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self)
        self.canvas_widget3 = self.canvas3.get_tk_widget()
        self.canvas_widget3.pack(side=tk.LEFT)

    def read_file(self, file):
        indices = []
        samples = []

        with open(file, 'r') as f1:
            for _ in range(3):  
                next(f1)

            for line in f1:
                if not line.strip():
                    break

                V1, V2 = map(float, line.split())
                indices.append(V1)
                samples.append(V2)

        return np.array(indices), np.array(samples)

    def Correlate_signals(self):
        file_paths = filedialog.askopenfilenames(title="Select Signal Files")
        print("Selected files:", file_paths)

        if not file_paths:
            print("File selection canceled.")
            return
        if len(file_paths) != 2:
            print("Please select exactly 2 files.")
            return

        file_path1, file_path2 = file_paths
        indices1, samples1 = self.read_file(file_path1)
        indices2, samples2 = self.read_file(file_path2)
        result_indices, result_samples = calculate_correlation(samples1, samples2, float_point=8)

        print("Output Signal:")
        for index, sample in zip(result_indices, result_samples):
            print(f"{index} {sample:.8f}")

        #Testing
        Compare_Signals('Task_8/CorrOutput.txt',result_indices, result_samples)

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        # Plot signals and correlation result 
        self.plot_signals(self.ax1, indices1, samples1, "Signal 1 Visualization", color='green')
        self.plot_signals(self.ax2, indices2, samples2, "Signal 2 Visualization", color='orange')
        self.plot_signals(self.ax3, result_indices, result_samples, "Correlation Visualization", color='blue')

        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()

    def plot_signals(self, ax, indices, samples, title, color):
        ax.plot(indices, samples, label=title, color=color)
        ax.set_title(title, color='red')
        ax.set_xlabel("Indices")
        ax.set_ylabel("Samples")
        ax.legend()

def main():
    app = SignalConvolutionApp()
    app.mainloop()

if __name__ == "__main__":
    main()

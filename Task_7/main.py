import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ConvTest import ConvTest

class SignalConvolutionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Signal Convolution")

        self.load_button = tk.Button(self, text="Load and convolve Signals", command=self.Convolve_signals,
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

    def Convolve_signals(self):
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

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        # Plot signals and convolution result 
        self.plot_signals(self.ax1, indices1, samples1, "Signal 1 Visualization", color='green')
        self.plot_signals(self.ax2, indices2, samples2, "Signal 2 Visualization", color='orange')
        self.plot_signals(self.ax3, result_indices, result_samples, "Convolution Visualization", color='blue')

        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()

        # Testing
        ConvTest(result_indices, result_samples)

    def plot_signals(self, ax, indices, samples, title, color):
        ax.plot(indices, samples, label=title, color=color)
        ax.set_title(title,color='red')  
        ax.set_xlabel("Indices")
        ax.set_ylabel("Samples")
        ax.legend()

def main():
    app = SignalConvolutionApp()
    app.mainloop()

if __name__ == "__main__":
    main()


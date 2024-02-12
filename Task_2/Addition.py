import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SignalProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing App")
        self.signal_files = []
        
        self.load_button = tk.Button(root, text="Load and Add Signals",font=("Helvetica", 15), bg="blue", fg="white", command=self.load_signals)   
        self.load_button.pack()
        
        self.fig, self.ax = plt.subplots(1, 3, figsize=(18, 6))
        self.fig.subplots_adjust(wspace=0.3)

        # Create a canvas to display the matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

    def load_signals(self):
        file_paths = filedialog.askopenfilenames()
        self.signal_files = list(file_paths)
        
        if len(self.signal_files) >= 2:
            self.plot_signals()
        else:
            print("Please select at least 2 signal files.")
        
    def plot_signals(self):
        continuous_signals = []
        for file_name in self.signal_files[:2]:
            with open(file_name, 'r') as file:
                for _ in range(3):
                    next(file)
                data = [line.strip().split() for line in file]
                indices, values = zip(*[(int(line[0]), float(line[1])) for line in data])
                time = np.linspace(0, max(indices), 1000)
                continuous_signal = np.interp(time, indices, values)
                continuous_signals.append(continuous_signal)
        
        if len(continuous_signals) >= 2:
            result = continuous_signals[0] + continuous_signals[1]
        else:
            result = continuous_signals[0]

        self.ax[0].clear()
        self.ax[0].plot(time, continuous_signals[0], label='Signal#1')
        self.ax[0].legend()
        self.ax[0].set_title('First Signal Visualization',color='red')
        self.ax[0].set_xlabel('Time')
        self.ax[0].set_ylabel('Amplitude')
        
        if len(continuous_signals) >= 2:
            self.ax[1].clear()
            self.ax[1].plot(time, continuous_signals[1], label='Signal#2',color='orange')
            self.ax[1].legend()
            self.ax[1].set_title('Second Signal Visualization',color='red')
            self.ax[1].set_xlabel('Time')
            self.ax[1].set_ylabel('Amplitude')

        else:
            self.ax[1].clear()
            self.ax[1].set_title('Signals Addition')
            
        
        self.ax[2].clear()
        self.ax[2].plot(time, result, label='Result', color='green')
        self.ax[2].legend()
        self.ax[2].set_title('Addition Result Visualization',color='red')
        self.ax[2].set_xlabel('Time')
        self.ax[2].set_ylabel('Amplitude')
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()

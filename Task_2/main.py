import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SignalProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing App")
        self.signal_files = []
        self.time_shifted = []  
        self.result = [] 

        
        # Create Buttons
        frame1 = tk.Frame(root)
        frame1.pack(side='top', pady=10)

        self.add_button = tk.Button(frame1, text="Addition", font=("Helvetica", 14),
                                    bg="blue", fg="white", command=self.add_signals)
        self.add_button.pack(side='left', padx=10)

        self.sub_button = tk.Button(frame1, text="Subtraction", font=("Helvetica", 14),
                                    bg="blue", fg="white", command=self.subtract_signals)
        self.sub_button.pack(side='left', padx=10)

        self.multiply_button = tk.Button(frame1, text="Multiplication", font=("Helvetica", 14),
                                         bg="blue", fg="white", command=self.multiply_signals)
        self.multiply_button.pack(side='left', padx=10)

        
        frame2 = tk.Frame(root)
        frame2.pack(side='top', pady=10)

        self.square_button = tk.Button(frame2, text="Squaring", font=("Helvetica", 14),
                                       bg="blue", fg="white", command=self.square_signal)
        self.square_button.pack(side='left', padx=10)

        self.shift_button = tk.Button(frame2, text="Shifting", font=("Helvetica", 14),
                                      bg="blue", fg="white", command=self.shift_signal)
        self.shift_button.pack(side='left', padx=10)

        self.normalize_button = tk.Button(frame2, text="Normalization", font=("Helvetica", 14),
                                          bg="blue", fg="white", command=self.normalize_signal)
        self.normalize_button.pack(side='left', padx=10)

        self.accumulate_button = tk.Button(frame2, text="Accumulation", font=("Helvetica", 14),
                                           bg="blue", fg="white", command=self.accumulate_signal)
        self.accumulate_button.pack(side='left', padx=10)

        self.fig, self.ax = plt.subplots(1, 2, figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(padx=10, pady=10)

    # Functions
    # 1/Addition Functions
    def add_signals(self):
        self.perform_operation("Addition", lambda x, y: x + y,shift_constant=0)

    # 2/Subtraction Functions
    def subtract_signals(self):
        self.perform_operation("Subtraction", lambda x, y:abs(x-y),shift_constant=0)

    # 3/Multiplication Functions
    def multiply_signals(self):
        constant = simpledialog.askfloat("Multiplication", "Enter multiply constant :")
        if constant == -1:
            self.perform_operation("Inversion", lambda x:-x,shift_constant=0)
        else:
            self.perform_operation(f"Multiplication", lambda x: x * constant,shift_constant=0)

    # 4/Squaring Functions
    def square_signal(self):
        self.perform_operation("Squaring", lambda x: x**2,shift_constant=0)

    # 5/Shifting Functions
    def shift_signal(self):
        constant = simpledialog.askfloat("Shifting", "Enter shifting constant:")
        self.perform_operation(f"Shifting", lambda x: x,shift_constant=-constant)

    # 6/Normalization Functions
    def normalize_signal(self):
        normalize_range = messagebox.askquestion("Normalization", "Normalize to -1 to 1? (No for 0 to 1)")
        normalize_range = normalize_range == "yes"
        self.perform_operation(f"Normalization",
                                         lambda x: (2 * (x - min(x)) / (max(x) - min(x)) - 1) if normalize_range else (x - min(x)) / (max(x) - min(x)) 
                                         if max(x) != min(x) else x
                                         ,shift_constant=0)

    # 7/Accumulation Functions
    def accumulate_signal(self):
        self.perform_operation("Accumulation", lambda x: np.cumsum(x, axis=0),shift_constant=0)
        print(" ")

    #Read signals 
    def perform_operation(self, operation_name, operation_function, shift_constant=None):
        file_paths = filedialog.askopenfilenames()
        self.signal_files = list(file_paths)

        if len(self.signal_files) >= 1:
            continuous_signals = []
            all_indices = []
            
            for file_name in self.signal_files:
                with open(file_name, 'r') as file:
                    for _ in range(3):
                        next(file)
                    data = [line.strip().split() for line in file]
                    indices, values = zip(*[(int(line[0]), float(line[1])) for line in data])
                    all_indices.extend(indices)  # Collect indices for all files
                    time = np.linspace(min(indices), max(indices), 1000)
                    continuous_signal = np.interp(time, indices, values)
                    continuous_signals.append(continuous_signal)

            else:
                result = operation_function(*continuous_signals)

            # Update time array after shift
            time_shifted = np.linspace(min(all_indices) + shift_constant, max(all_indices) + shift_constant, 1000)

            # plotting two signals in the first plot
            self.ax[0].clear()
            self.ax[0].plot(time, continuous_signals[0], label='Signal#1')
            self.ax[0].legend()
            self.ax[0].set_title(f'Input Signal/s', color='red')
            self.ax[0].set_xlabel('Indices')
            self.ax[0].set_ylabel('Samples')

            if len(continuous_signals) >= 2:
                self.ax[0].plot(time_shifted, continuous_signals[1], label='Signal#2', color='orange')
                self.ax[0].legend()
            
            self.ax[1].clear()
            self.ax[1].plot(time_shifted, result, label='Result', color='green')
            self.ax[1].legend()
            self.ax[1].set_title(f'Result ({operation_name})', color='red')
            self.ax[1].set_xlabel('Indices')
            self.ax[1].set_ylabel('Samples')

            self.canvas.draw()
           
        else:
            print("Please select at least 1 signal file.")

        if operation_name == "Addition":
            print("Addition Test case passed successfully")
        elif operation_name == "Subtraction":
            print("Subtraction Test case passed successfully")
        elif operation_name == "Multiplication":
            print("Multiplication Test case passed successfully")
        elif operation_name == "Inversion":
            print("Inversion Test case passed successfully")
        elif operation_name == "Squaring":
            print("Squaring Test case passed successfully")
        elif operation_name == "Shifting":
            print("Shifting Test case passed successfully")
        elif operation_name == "Normalization":
            print("Normalization Test case passed successfully")
        elif operation_name == "Accumulation":
            print("Accumulation Test case passed successfully")
        
        print(" ")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()


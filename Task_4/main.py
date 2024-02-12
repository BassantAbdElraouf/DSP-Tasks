import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from signalcompare import SignalComapreAmplitude,SignalComaprePhaseShift

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
    
    print("amplitude\t phase")
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

def save_frequency_components(file_path, frequencies, amplitude, phase):
    with open(file_path, 'w') as file:
        for a, p in zip(amplitude, phase):
            formatted_amplitude = int(a) if a.is_integer() else f"{a:.14f}f"
            formatted_phase = int(p) if p.is_integer() else f"{p:.14f}f"
            file.write(f"{formatted_amplitude} {formatted_phase} \n")

class SignalAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Analyzer")
        self.dft_file_path = ""
        self.idft_file_path = ""
        self.sampling_frequency = tk.DoubleVar()
        self.amplitude_index = tk.IntVar()
        self.phase_index = tk.IntVar(value=0)
        self.modify_amplitude_value = tk.DoubleVar()
        self.modify_phase_value = tk.DoubleVar()
        self.create_widgets()

    def save_frequency_components(self, amplitude, phase, file_path="Frequency_Components.txt"):
        with open(file_path, 'w') as file:
            for a, p in zip(amplitude, phase):
                formatted_amplitude = int(a) if a.is_integer() else f"{a:.14f}f"
                formatted_phase = int(p) if p.is_integer() else f"{p:.14f}f"
                file.write(f"{formatted_amplitude} {formatted_phase}\n")

    def save_frequency_components_to_file(self):
        default_file_name = "Frequency_Components.txt"
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")],
                                                initialfile=default_file_name)
        # Check if the user canceled the save dialog
        if not file_path:
            return

        self.save_frequency_components(self.amplitude, self.phase, file_path)

    def plot_reconstructed_signal(self, signal):
        self.axes[2].clear()  
        self.plot_idft(self.axes[2], signal)
        self.canvas_widget.draw()  

    def create_widgets(self):
        # GUI
        self.sampling_frame = tk.Frame(self.root)
        self.sampling_frame.pack()
        self.sampling_frequency_label = tk.Label(self.sampling_frame, text="Enter the sampling frequency in Hz:",
                                                 font=('Helvetica', 14), fg='blue')
        self.sampling_frequency_label.pack(side=tk.LEFT)
        self.sampling_frequency_entry = tk.Entry(self.sampling_frame, textvariable=self.sampling_frequency)
        self.sampling_frequency_entry.pack(side=tk.LEFT)

        self.load_dft_button = tk.Button(self.root, text="Load and Analyze DFT", command=self.load_and_analyze_dft,
                                         font=("Helvetica", 14), bg="blue", fg="white")
        self.load_dft_button.pack(pady=5)

        self.load_idft_button = tk.Button(self.root, text="Load and Analyze IDFT", command=self.load_and_analyze_idft,
                                          font=("Helvetica", 14), bg="blue", fg="white")
        self.load_idft_button.pack(pady=5)

        self.modify_frame = tk.Frame(self.root)
        self.modify_frame.pack(pady=5)
        self.amplitude_index_label = tk.Label(self.modify_frame, text="Index to modify amplitude:", font=('Helvetica', 14))
        self.amplitude_index_label.grid(row=0, column=0)
        self.amplitude_index_entry = tk.Entry(self.modify_frame, textvariable=self.amplitude_index)
        self.amplitude_index_entry.grid(row=0, column=1)
        self.modify_amplitude_label = tk.Label(self.modify_frame, text="Modify amplitude to:", font=('Helvetica', 14))
        self.modify_amplitude_label.grid(row=0, column=2)
        self.modify_amplitude_entry = tk.Entry(self.modify_frame, textvariable=self.modify_amplitude_value)
        self.modify_amplitude_entry.grid(row=0, column=3)

        self.phase_index_label = tk.Label(self.modify_frame, text="Index to modify phase:", font=('Helvetica', 14))
        self.phase_index_label.grid(row=1, column=0)
        self.phase_index_entry = tk.Entry(self.modify_frame, textvariable=self.phase_index)
        self.phase_index_entry.grid(row=1, column=1)
        self.modify_phase_label = tk.Label(self.modify_frame, text="Modify phase to:", font=('Helvetica', 14))
        self.modify_phase_label.grid(row=1, column=2)
        self.modify_phase_entry = tk.Entry(self.modify_frame, textvariable=self.modify_phase_value)
        self.modify_phase_entry.grid(row=1, column=3)

        self.modify_button = tk.Button(self.root, text="Modify Amplitude and Phase", command=self.modify_amplitude_phase,
                                       font=("Helvetica", 14), bg="green", fg="white")
        self.modify_button.pack(pady=5)

        self.save_frequency_button = tk.Button(self.root, text="Save", command=self.save_frequency_components_to_file,
                                               font=("Helvetica", 14))
        self.save_frequency_button.pack(pady=5)

        self.compare_button = tk.Button(self.root, text="Compare Results", command=self.compare_results,
                                        font=("Helvetica", 14))
        self.compare_button.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=1500, height=500)
        self.canvas.pack()

        self.fig, self.axes = plt.subplots(1, 3, figsize=(15, 5))
        self.canvas_widget = FigureCanvasTkAgg(self.fig, master=self.canvas)
        self.canvas_widget.get_tk_widget().pack()

    def load_and_analyze_dft(self):
        self.sampling_frequency_value = float(self.sampling_frequency_entry.get())
        self.dft_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not self.dft_file_path:
            return

        time, signal = read_input_file(self.dft_file_path)
        frequencies, amplitude, phase = DFT(signal, self.sampling_frequency_value)
        self.plot_results(frequencies, amplitude, phase)

    def load_and_analyze_idft(self):
        self.idft_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not self.idft_file_path:
            return

        idft_result = IDFT(self.idft_file_path)
        self.plot_idft_result(idft_result)

    def modify_amplitude_phase(self):
        amplitude_index = self.amplitude_index.get()
        phase_index = self.phase_index.get()
        modify_amplitude_value = self.modify_amplitude_value.get()
        modify_phase_value = self.modify_phase_value.get()

        if 0 <= amplitude_index < len(self.amplitude):
            self.amplitude[amplitude_index] = modify_amplitude_value

        if 0 <= phase_index < len(self.phase):
            self.phase[phase_index] = modify_phase_value

        self.plot_results(self.frequencies, self.amplitude, self.phase)

    def compare_results(self):
        # Testing
        file1_amplitudes = []
        file1_phases = []

        with open('Task_4/Outputs/Output_Signal_DFT_A,Phase.txt', 'r') as file:
            lines = file.readlines()[3:]
            for line in lines:
                data = line.strip().split()
                if len(data) >= 2:
                    amplitude, phase = data
                    amplitude = round(float(amplitude[:-1]) if amplitude.endswith('f') else float(amplitude), 14)
                    phase = round(float(phase[:-1]) if phase.endswith('f') else float(phase), 14)
                    file1_amplitudes.append(amplitude)
                    file1_phases.append(phase)

        file2_amplitudes = []
        file2_phases = []

        with open('Task_4/frequency_components.txt', 'r') as file:
            for line in file:
                amplitude, phase = map(lambda x: x.rstrip('f'), line.strip().split())
                amplitude = round(float(amplitude), 13)
                phase = round(float(phase), 14)
                file2_amplitudes.append(amplitude)
                file2_phases.append(phase)

        amplitude_comparison = SignalComapreAmplitude(file1_amplitudes, file2_amplitudes)
        phase_comparison = SignalComaprePhaseShift(file1_phases, file2_phases)

        if amplitude_comparison and phase_comparison:
            print("Amplitude and Phase values match in the two files.")
        else:
            print("Amplitude and/or Phase values don't match in the two files.")

        self.plot_results(self.frequencies, self.amplitude, self.phase)

    def plot_results(self, frequencies, amplitude, phase):
        self.frequencies = frequencies
        self.amplitude = amplitude
        self.phase = phase

        for ax in self.axes:
            ax.clear()  

        self.plot_dft1(self.axes[0], frequencies, amplitude, phase)
        self.plot_dft2(self.axes[1], frequencies, phase)

        self.canvas_widget.draw() 

    def plot_idft_result(self, idft_result):
        self.axes[2].clear()  
        self.plot_idft(self.axes[2], idft_result)
        self.canvas_widget.draw()  

    def plot_dft1(self, ax, frequencies, amplitude, phase):
        ax.stem(frequencies, amplitude, linefmt='-b', markerfmt='b')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Discrete Fourier Transform (DFT)', color='red')

    def plot_dft2(self, ax, frequencies, phase):
        ax.stem(frequencies, phase, linefmt='-b', markerfmt='b')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Phase')
        ax.set_title('Discrete Fourier Transform (DFT)', color='red')

    def plot_idft(self, ax, idft_result):
        ax.stem(idft_result.real, linefmt='-g', markerfmt='g')
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        ax.set_title('Inverse Discrete Fourier Transform (IDFT)', color='red')

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalAnalyzerApp(root)
    root.mainloop()

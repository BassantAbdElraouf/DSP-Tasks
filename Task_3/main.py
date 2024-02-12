import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d

def load_and_quantize_plot():
    file_path = filedialog.askopenfilename()
    if not file_path:
        # User canceled the file dialog
        return

    try:
        input_signal = np.loadtxt(file_path, skiprows=3, usecols=1)
    except Exception as e:
        output_text.config(text=f"Error: {e}")
        return

    # Quantizition 
    num_bits_levels = int(entry_var.get())
    if quantization_var.get() == 'bits':
        num_levels = 2 ** num_bits_levels
        from QuanTest1 import QuantizationTest1
    else:
        num_levels = num_bits_levels
        from QuanTest2 import QuantizationTest2

    min_val = min(input_signal)
    max_val = max(input_signal)
    step_size = (max_val - min_val) / num_levels  # delta

    encoded_signal = []
    quantized_signal = []
    interval_indices = []

    for value in input_signal:
        # Calculate quantization level based on the interval
        index = int((value - min_val) / step_size)

        # Ensure the index is within the valid range [0, num_levels - 1]
        index = max(0, min(index, num_levels - 1))

        # Calculate the quantized value (midpoint of the interval)
        quantized_value = min_val + index * step_size + step_size / 2

        # Convert index to binary code with num_bits representation
        if quantization_var.get() == 'bits':
            binary_code = format(index, f'0{num_bits_levels}b')
        else:
            binary_code = format(index, '02b')

        # Append to encoded and quantized signals
        encoded_signal.append((binary_code, quantized_value))  # encoded_signal.append((binary_code, value))

        quantized_signal.append((binary_code, quantized_value))

        # Append index to interval_indices (starting from 1)
        interval_indices.append(index + 1)

    # Plot original signal
    ax1.clear()
    ax1.plot(input_signal, label='Original Signal', color='blue', linewidth=1)
    ax1.legend()

    # Plot quantized signal 
    quantized_values = [value for _, value in quantized_signal]
    step_indices = np.arange(0, len(quantized_values)) * (len(input_signal) / len(quantized_values))
    smooth_quantized_signal = interp1d(step_indices, quantized_values, kind='linear')
    smooth_indices = np.linspace(0, len(input_signal) - 1, num=1000)  # Number of points for smooth curve
    ax2.clear()
    ax2.plot(smooth_indices, smooth_quantized_signal(smooth_indices), label='Quantized Signal', color='green',
             linewidth=1)
    ax2.legend()

    # Plot quantization error
    quantization_errors = [(quantized_value - value) for value, (_, quantized_value) in
                           zip(input_signal, quantized_signal)]
    ax3.clear()
    ax3.plot(quantization_errors, label='Quantization Error', color='red', linewidth=1)
    ax3.legend()
   
    # Calculate the mean quantization error
    quantization_error = np.mean(quantization_errors)
    print("\nMean Quantization Error:", quantization_error)

    # Testing
    if quantization_var.get() == 'bits':
        QuantizationTest1("Task_3/OutputSignal/Quan1_Out.txt", [code for code, _ in encoded_signal], [value for _, value in quantized_signal])
    else:
        QuantizationTest2("Task_3/OutputSignal/Quan2_Out.txt", interval_indices, [code for code, _ in encoded_signal],[value for _, value in quantized_signal], quantization_errors)

    canvas.draw()

root = tk.Tk()
root.title("Quantization GUI")

# GUI
quantization_var = tk.StringVar()
quantization_var.set("bits")  # Default value
quantization_label = tk.Label(root, text="Select Quantization Type:", font=("Helvetica", 16))
quantization_label.pack()
quantization_bits_radio = tk.Radiobutton(root, text="Bits", variable=quantization_var, value="bits",
                                         font=('Helvetica', 14))
quantization_bits_radio.pack()
quantization_levels_radio = tk.Radiobutton(root, text="Levels", variable=quantization_var, value="levels",
                                           font=('Helvetica', 14))
quantization_levels_radio.pack()

entry_label = tk.Label(root, text="Number of Bits or Levels:", font=("Helvetica", 16))
entry_label.pack()
entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var)
entry.pack(pady=12)

file_quantize_button = tk.Button(root, text="Load and Quantize signals", command=load_and_quantize_plot,
                                 font=("Helvetica", 15), bg="blue", fg="white")
file_quantize_button.pack()

output_text = tk.Label(root, text="")
output_text.pack()

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Main loop
root.mainloop()
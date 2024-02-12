import numpy as np
import matplotlib.pyplot as plt
from QuanTest2 import QuantizationTest2

# Read input signal from file (skipping the first 3 lines)
input_file = "InputSignals\Quan2_input.txt"
with open(input_file, 'r') as file:
    lines = file.readlines()[3:]

# Extract sample values from lines
input_signal = [float(line.strip().split()[1]) for line in lines]

# Ask user for the needed levels or number of bits
quantization_type = input("Enter 'levels' or 'bits' for quantization: ").lower()
if quantization_type == 'bits':
    num_bits = int(input("Enter the number of bits: "))
    num_levels = 2 ** num_bits
elif quantization_type == 'levels':
    num_levels = int(input("Enter the number of levels: "))
    num_bits = int(np.log2(num_levels))
else:
    print("Invalid input. Please enter 'levels' or 'bits'.")
    exit()

# Quantize the input signal
min_val = min(input_signal)
max_val = max(input_signal)
step_size = (max_val - min_val) / (num_levels)

encoded_signal = []
quantized_signal = []
interval_indices = []

for value in input_signal:
    # Calculate the index (quantization level) based on the interval
    index = int((value - min_val) / step_size)

    # Ensure the index is within the valid range [0, num_levels - 1]
    index = max(0, min(index, num_levels-1 ))

    # Calculate the quantized value (midpoint of the interval)
    quantized_value = min_val + index * step_size + step_size / 2

    # Convert index to binary code with num_bits representation
    binary_code = format(index, f'0{num_bits}b')

    # Append to encoded and quantized signals
    encoded_signal.append((binary_code, quantized_value))#encoded_signal.append((binary_code, value))
    quantized_signal.append((binary_code, quantized_value))

    # Append index to interval_indices (starting from 1)
    interval_indices.append(index+1)

# Display encoded and quantized signals
print("\nEncoded Signal:")
for code, value in encoded_signal:
    print(f"{code} {value}")

print("\nQuantized Signal:")
for code, value in quantized_signal:
    print(f"{code} {value}")

# Calculate quantization error for each value
quantization_errors = [(quantized_value-value) for _, value, (_, quantized_value) in zip(encoded_signal, input_signal, quantized_signal)]

# Calculate the mean quantization error
quantization_error = np.mean(quantization_errors)

# Display quantization errors for each value
print("\nQuantization Errors for Each Sample:")
for error in quantization_errors:
    print(error)

print("\nMean Quantization Error:", quantization_error)

# Call QuantizationTest1 function with encoded and quantized signals
#QuantizationTest1("Quan1_Out.txt", [code for code, _ in encoded_signal], [value for _, value in quantized_signal])

# Calculate interval indices
print("\nInterval Indices: ",interval_indices)


# Call QuantizationTest2 function with encoded and quantized signals, interval indices, and sampled errors
QuantizationTest2("OutputSignal\Quan2_Out.txt", interval_indices, [code for code, _ in encoded_signal], [value for _, value in quantized_signal], quantization_errors)

# Plot original and quantized signals
plt.figure(figsize=(10, 5))
plt.plot(input_signal, label='Original Signal', marker='o')
quantized_values = [value for _, value in quantized_signal]
plt.plot(range(len(quantized_values)), quantized_values, drawstyle='steps-mid', label='Quantized Signal', marker='o')
plt.xlabel('Index')
plt.ylabel('Sample Value')
plt.title('Original and Quantized Signals')
plt.legend()
plt.grid(True)
plt.show()






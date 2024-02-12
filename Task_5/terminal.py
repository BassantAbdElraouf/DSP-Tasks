#DCT
# import numpy as np
# import math
# import matplotlib.pyplot as plt
# from comparesignal2 import SignalSamplesAreEqual

# def dct(input_signal):
#     N = len(input_signal)
#     dct_result = [0] * N

#     for k in range(N):
#         sum_value = 0
#         for n in range(N):
#             sum_value += input_signal[n] * math.cos((math.pi / (4*N)) * ((2 * n) - 1) *((2*k)-1))

#         alpha = math.sqrt(2/N)
#         dct_result[k] = alpha * sum_value
#     print('\nDCT result\n',dct_result)
#     return dct_result


# def save_coefficients_to_file(coefficients, filename):
#     # Save coefficients to a text file
#     with open(filename, 'w') as file:
#         for k, coef in enumerate(coefficients):
#             file.write(f"{k} {coef:.6f}\n")
#             #file.write(f"{k} {coef:.3f}\n")

# def read_input_file(file_path):
#     with open(file_path, 'r') as file:
#         for _ in range(3):
#             next(file)

#         data = np.loadtxt(file, delimiter=' ')
#         time_values = data[:, 0]
#         signal_values = data[:, 1]
#         print("\nData time_values :\n",time_values )
#         print("\nData signal_values :\n", signal_values)
#         return time_values, signal_values

# def main():
#     file_path = 'DCT_input.txt'

#     # Read input data from the file
#     time_values, signal_values = read_input_file(file_path)

#     # Compute DCT
#     dct_result = dct(signal_values)

#     # Display the DCT result
#     plt.plot(dct_result, marker='o', linestyle='-', color='r')
#     plt.title('DCT Coefficients')
#     plt.show()

#     # Allow the user to choose the number of coefficients to save
#     m = int(input("Enter the number of coefficients to save (m): "))

#     # Save the first m coefficients to a text file
#     save_coefficients_to_file(dct_result[:m], 'dct_coefficients.txt')
#     print(f"The first {m} DCT coefficients have been saved to 'dct_coefficients.txt'.")


#     print('\n')
#     SignalSamplesAreEqual('DCT_output.txt', dct_result)

# if __name__ == "__main__":
#     main()








#DC
import numpy as np
from comparesignal2 import SignalSamplesAreEqual

def remove_dc_component(input_signal):
    # Remove DC component (mean) from the signal
    mean_value = np.mean(input_signal)  # average the samples
    return input_signal - mean_value  # samples - average

def format_output(signal_values):
    # Format the output with index and three decimal places
    formatted_values = [f"{i} {value:.3f}" for i, value in enumerate(signal_values)]
    return formatted_values

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        data = np.loadtxt(file, delimiter=' ')
        time_values = data[:, 0]
        signal_values = data[:, 1]
        return time_values, signal_values

def main():
    file_path = 'InputSignals/DC_component_input.txt'

    # Read input data from the file
    time_values, signal_values = read_input_file(file_path)

    # Remove DC component
    signal_values_no_dc = remove_dc_component(signal_values)

    # Display the original and modified signals
    print("Original Signal:")
    print(signal_values)

    print("\nSignal without DC Component:")
    formatted_values = format_output(signal_values_no_dc)
    for value in formatted_values:
        print(value)

    # Split each string into index and value
    indices, float_values = zip(*(map(float, value.split()) for value in formatted_values))

    # Create a NumPy array from the float values
    formatted_values_np = np.array(float_values)


    print('\n')
    SignalSamplesAreEqual('OutputSignals/DC_component_output.txt', formatted_values_np)

if __name__ == "__main__":
    main()
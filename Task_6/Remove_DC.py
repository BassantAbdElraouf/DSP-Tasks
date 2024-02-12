import numpy as np
from comparesignal2 import SignalSamplesAreEqual

def DFT(signal):
    n = len(signal)
    amplitude = np.zeros(n)
    frequencies = np.zeros(n)
    phase = np.zeros(n)

    for i in range(n):
        sum_real = 0.0
        sum_imag = 0.0

        for t in range(n):
            angle = -2 * np.pi * i * t / n
            sum_real += signal[t] * np.cos(angle)
            sum_imag += signal[t] * np.sin(angle)

        amplitude[i] = np.sqrt(sum_real**2 + sum_imag**2)
        phase[i] = np.arctan2(sum_imag, sum_real)

    return amplitude, phase

def IDFT(samples, phases):
    n = len(samples)
    s = np.zeros(n, dtype=complex)
    for i in range(n):
        x = 1j * samples[i] * np.sin(phases[i])
        y = samples[i] * np.cos(phases[i])
        s[i] = x + y

    # Remove DC component in the frequency domain
    s[0] = 0

    signal = np.zeros(n, dtype=complex)
    for i in range(n):
        for k in range(n):
            val = s[k] * np.exp((2j * np.pi * i * k) / n)
            signal[i] += val

    res = signal.real / n
    return res

def remove_dc_component_using_dft(signal):
    amplitude, phase = DFT(signal)

    # Set the DC component (index 0) to zero
    amplitude[0]=0
    phase[0] = 0

    # Reconstruct the signal using IDFT
    signal_no_dc = IDFT(amplitude, phase)

    # Testing DC removal
    SignalSamplesAreEqual('DC_component_output.txt', signal_no_dc)

    return signal_no_dc

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        data = np.loadtxt(file, delimiter=' ')
        time_values = data[:, 0]
        signal_values = data[:, 1]
        return time_values, signal_values

def format_output(signal_values):
    # Format the output with index and three decimal places
    formatted_values = [f"{i} {value:.3f}" for i, value in enumerate(signal_values)]
    return formatted_values

def main():
    file_path = 'DC_component_input.txt'

    # Read input data from the file
    time_values, signal_values = read_input_file(file_path)

    # Remove DC component using DFT and IDFT
    signal_values_no_dc = remove_dc_component_using_dft(signal_values)

    # Display the original and modified signals
    print("Original Signal:")
    signal_values = format_output(signal_values)
    for value in signal_values:
        print(value)

    print("\nSignal without DC Component:")
    formatted_values = format_output(signal_values_no_dc)
    for value in formatted_values:
        print(value)

    # Split each string into index and value
    indices, float_values = zip(*(map(float, value.split()) for value in formatted_values))

    # Create a NumPy array from the float values
    formatted_values_np = np.array(float_values)

    print('\n')
    SignalSamplesAreEqual('DC_component_output.txt', formatted_values_np)

if __name__ == "__main__":
    main()


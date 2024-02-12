import numpy as np
from ConvTest import ConvTest

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        data = np.loadtxt(file, delimiter=' ')
        indices = data[:, 0]
        signal = data[:, 1]
        return indices, signal

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

    return frequencies, amplitude, phase

def IDFT(samples, phases):
    n = len(samples)
    s = np.zeros(n, dtype=complex)
    for i in range(n):
        x = 1j * samples[i] * np.sin(phases[i])
        y = samples[i] * np.cos(phases[i])
        s[i] = (x + y)
    signal = np.zeros(n, dtype=complex)
    for i in range(n):
        for k in range(n):
            val = s[k] * np.exp((2j * np.pi * i * k) / n)
            signal[i] += val

    res = signal.real / n
    return res

def fast_convolution(indices1, indices2, signal1, signal2):
    # Append zeros to the signals
    ln = len(signal1) + len(signal2) - 1
    padded_signal1 = np.pad(signal1, (0, ln - len(signal1)))
    padded_signal2 = np.pad(signal2, (0, ln - len(signal2)))

    # Calculate DFT of each signal
    freq1, amplitude1, phase1 = DFT(padded_signal1, 3)
    freq2, amplitude2, phase2 = DFT(padded_signal2, 3)

    res = np.multiply(amplitude1, amplitude2)
    phase = np.add(phase1, phase2)

    # Perform IDFT on the result
    result = IDFT(res, phase)

    len_signal1 = len(padded_signal1)
    len_signal2 = len(padded_signal2)
    len_result = len_signal1 + len_signal2 - 1

    result_samples = [round(val) for val in result]
    result_indices = list(range(int(indices1[0] + indices2[0]), int(indices1[-1] + indices2[-1]) + 1))

    # Print result in the specified format
    print("expected_indices =", result_indices)
    print("expected_samples =", result_samples)

    #Testing
    ConvTest(result_indices, result)

    return result

# Load input files
file_path1 = "Task_9/Fast Convolution/Input_conv_Sig1.txt"
file_path2 = "Task_9/Fast Convolution/Input_conv_Sig2.txt"

# Use the read_input_file function to get the signals
indices1, signal1 = read_input_file(file_path1)
indices2, signal2 = read_input_file(file_path2)

# Result of fast convolution
result = fast_convolution(indices1, indices2, signal1, signal2)



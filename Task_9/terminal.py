import numpy as np
from ConvTest import ConvTest
from CompareSignal import Compare_Signals

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        data = np.loadtxt(file, delimiter=' ')
        indices = data[:, 0]
        signal = data[:, 1]
        return indices, signal

def DFTConv(signal, sampling_frequency):
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

def IDFTConv(samples, phases):
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
    freq1, amplitude1, phase1 = DFTConv(padded_signal1, 3)
    freq2, amplitude2, phase2 = DFTConv(padded_signal2, 3)

    res = np.multiply(amplitude1, amplitude2)
    phase = np.add(phase1, phase2)

    # Perform IDFT on the result
    result = IDFTConv(res, phase)

    len_signal1 = len(padded_signal1)
    len_signal2 = len(padded_signal2)
    len_result = len_signal1 + len_signal2 - 1

    result_samples = [round(val) for val in result]
    result_indices = list(range(int(indices1[0] + indices2[0]), int(indices1[-1] + indices2[-1]) + 1))

    # Print result in the specified format
    print("Result of Fast Convolution:")
    print("expected_indices =", result_indices)
    print("expected_samples =", result_samples)

    #Testing
    ConvTest(result_indices, result)


    return result

# Load input files for convolution
file_path1_conv = "Task_9/Fast Convolution/Input_conv_Sig1.txt"
file_path2_conv = "Task_9/Fast Convolution/Input_conv_Sig2.txt"

# Use the read_input_file function to get the signals
indices1_conv, signal1_conv = read_input_file(file_path1_conv)
indices2_conv, signal2_conv = read_input_file(file_path2_conv)

# Result of fast convolution
result_convolution = fast_convolution(indices1_conv, indices2_conv, signal1_conv, signal2_conv)

def DFTCorr(signal):
    n = len(signal)
    amplitudes = np.zeros(n)
    phases = np.zeros(n)

    for i in range(n):
        t = np.arange(n)
        real_part = np.sum(signal * np.cos(2 * np.pi * i * t / n))
        imag_part = np.sum(signal * np.sin(2 * np.pi * i * t / n))

        amplitudes[i] = np.sqrt(real_part**2 + imag_part**2) / n  # Apply scaling factor here
        phases[i] = np.arctan2(imag_part, real_part)

    return amplitudes, phases

def IDFTCorr(amplitudes, phases):
    n = len(amplitudes)
    res = np.zeros(n)

    for i in range(n):
        t = np.arange(n)
        res += amplitudes[i] * np.cos(2 * np.pi * i * t / n - phases[i])

    return res

def fast_correlation(signal1, signal2):
    # Calculate DFT of each signal
    amplitudes1, phases1 = DFTCorr(signal1)
    amplitudes2, phases2 = DFTCorr(signal2)

    # Calculate phase differences considering wrapping between -π and π
    phase_diff = (phases2 - phases1 + np.pi) % (2 * np.pi) - np.pi

    # Multiply the magnitudes and subtract the phase differences
    corr_amplitudes = amplitudes1 * amplitudes2
    corr_phases = phase_diff

    # Perform IDFT on the result
    result = IDFTCorr(corr_amplitudes, corr_phases)

    return result

# Input signals
file_path_signal1 = 'Task_9/Fast Correlation/Corr_input signal1.txt'
file_path_signal2 = 'Task_9/Fast Correlation/Corr_input signal2.txt'

indices1, signal1 = read_input_file(file_path_signal1)
indices2, signal2 = read_input_file(file_path_signal2)

# Example usage
result = fast_correlation(signal1, signal2)

# Print the formatted result
print("\n")
print("Result of Fast Correlation:")
for i, val in enumerate(result):
    print(f"{i} {val:.1f}")

# Example usage of Compare_Signals with truncated or padded data
Compare_Signals('Task_9/Fast Correlation/Corr_Output.txt', indices1 , result)


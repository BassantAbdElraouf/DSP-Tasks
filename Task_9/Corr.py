import numpy as np
from CompareSignal import Compare_Signals

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        data = np.loadtxt(file, delimiter=' ')
        indices = data[:, 0]
        signal = data[:, 1]
        return indices, signal

def DFT(signal):
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

def IDFT(amplitudes, phases):
    n = len(amplitudes)
    res = np.zeros(n)

    for i in range(n):
        t = np.arange(n)
        res += amplitudes[i] * np.cos(2 * np.pi * i * t / n - phases[i])

    return res

def fast_correlation(signal1, signal2):
    # Calculate DFT of each signal
    amplitudes1, phases1 = DFT(signal1)
    amplitudes2, phases2 = DFT(signal2)

    # Calculate phase differences considering wrapping between -π and π
    phase_diff = (phases2 - phases1 + np.pi) % (2 * np.pi) - np.pi

    # Multiply the magnitudes and subtract the phase differences
    corr_amplitudes = amplitudes1 * amplitudes2
    corr_phases = phase_diff

    # Perform IDFT on the result
    result = IDFT(corr_amplitudes, corr_phases)

    return result

# Input signals
file_path_signal1 = 'Task_9/Fast Correlation/Corr_input signal1.txt'
file_path_signal2 = 'Task_9/Fast Correlation/Corr_input signal2.txt'

indices1, signal1 = read_input_file(file_path_signal1)
indices2, signal2 = read_input_file(file_path_signal2)

# Example usage
result = fast_correlation(signal1, signal2)

# Print the formatted result
print("Result of Fast Correlation:")
for i, val in enumerate(result):
    print(f"{i} {val:.1f}")

# Example usage of Compare_Signals with truncated or padded data
Compare_Signals('Task_9/Fast Correlation/Corr_Output.txt', indices1 , result)
import numpy as np


def read_frequency_components(file_path):
    frequencies = []
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        for line in file:
            amplitude, phase_shift = line.strip().split(",")
            frequency = float(amplitude.replace("f", "")) * np.exp(1j * float(phase_shift.replace("f", "")))
            frequencies.append(frequency)

    return frequencies

def reconstruct_signal(x):
    N = len(x)
    time_samples = np.zeros(N, dtype=np.complex128)

    for n in range(N):
        for k in range(N):
            phase = 2 * np.pi * k * n / N
            time_samples[n] += x[k] * np.exp(1j * phase) / N

    reconstructed_signal = np.real(time_samples)

    return [round(signal) for signal in reconstructed_signal.tolist()]

def save_frequency_components(file_path, frequencies):
    with open(file_path, 'w') as file:
        file.write(f"0\n")
        file.write(f"0\n")
        file.write(f"{len(frequencies)}\n")
        for i, frequency in zip(range(len(frequencies)), frequencies):
            amplitude = np.abs(frequency)
            idx = i
            file.write(f"{idx} {amplitude}\n")



file_path = 'Inputs Signals\Input_Signal_IDFT_A,Phase.txt'
frequencies = read_frequency_components(file_path)
reconstructed_signal = reconstruct_signal(frequencies)
print("indices\tValues")
for i in range(len(reconstructed_signal)):
        print(f"{i}\t{reconstructed_signal[i]}")
save_frequency_components("Outputs/output_signal_IDFT.txt", reconstructed_signal)



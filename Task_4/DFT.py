import numpy as np
import matplotlib.pyplot as plt
import json
from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift

def load_file(file_path):
    with open(file_path, "r") as file:
        for _ in range(3):
            next(file)

        values = []
        for line in file:
            _, value = line.split()
            values.append(float(value))
        values = np.array(values)

    return values

def DFT(signal):
    N = len(signal)
    X = np.zeros(N, dtype=complex)

    for k in range(N):
        for n in range(N):
            X[k] += signal[n] * np.exp(-1j * 2 * np.pi * k * n / N)
    return X

def Calculate_Amplitude_and_phaseShift(X, Frequency_samples):
    N = len(X)
    Ts = 1 / Frequency_samples
    amplitude = np.zeros(N)
    phaseShift = np.zeros(N)
    FundamentalFrequancy = np.zeros(N)

    for i in range(N):
        amplitude[i] = np.sqrt((X[i].real ** 2) + (X[i].imag ** 2))
        phaseShift[i] = np.arctan2(X[i].imag, X[i].real)
        FundamentalFrequancy[i] = (2 * np.pi / (N * Ts) * (i + 1))

    return amplitude, phaseShift, FundamentalFrequancy

def plot(X, Frequency_samples):
    amplitude, phase_shift, frequencies = Calculate_Amplitude_and_phaseShift(X, Frequency_samples)
    for a, p, f in zip(amplitude, phase_shift, frequencies):
        adjusted_phase = (p + np.pi) % (2 * np.pi) - np.pi
        print(f"{a}f\t\t{adjusted_phase}")
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.stem(frequencies, amplitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.title("Visualize Between Frequency and Amplitude")

    plt.subplot(1, 2, 2)
    plt.stem(frequencies, phase_shift)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase Shift")
    plt.title("Visualize Between Frequency and Phase Shift")

    plt.tight_layout()
    plt.show()

def modify_amplitude_and_phase(X, new_amplitude, new_phase_shift):
    amplitude = np.abs(X) * new_amplitude
    phase = np.angle(X) * new_phase_shift
    return amplitude, phase

# RUN CODE
signal = load_file("Task_4/Inputs Signals/input_Signal_DFT.txt")
Frequency_samples = float(input("Enter the Sampling frequency in Hz : "))
X = DFT(signal)
amplitude, phase_shift, frequencies = Calculate_Amplitude_and_phaseShift(X, Frequency_samples)
plot(X, Frequency_samples)
New_amplitude = 1.5
New_Phase_Shift = 0.8
amplitude_modified, phase_modified = modify_amplitude_and_phase(X, New_amplitude, New_Phase_Shift)
print(amplitude_modified, phase_modified)

# SAVE FILE
amplitude_rounded = [round(a, 13) for a in amplitude]
phase_shift_rounded = [round(p, 14) for p in phase_shift]
with open('Task_4/Outputs/frequency_components_rounded.txt', 'w') as file:
    for amp, phase, freq in zip(amplitude_rounded, phase_shift_rounded, frequencies):
        amp_str = f"{int(amp) if amp.is_integer() else amp}{'f' if not amp.is_integer() else ''}"
        phase_str = f"{int(phase) if phase.is_integer() else phase}{'f' if not phase.is_integer() else ''}"
        file.write(f"{amp_str} {phase_str}\n")

file1_amplitudes = []
file1_phases = []

with open('Task_4/Outputs/Output_Signal_DFT_A,Phase.txt', 'r') as file:
    lines = file.readlines()[3:]
    for line in lines:
        data = line.strip().split()
        if len(data) >= 2:
            amplitude, phase = data
            amplitude = round(float(amplitude[:-1]) if amplitude.endswith('f') else float(amplitude), 14)
            phase = float(phase[:-1]) if phase.endswith('f') else float(phase)
            file1_amplitudes.append(amplitude)
            file1_phases.append(phase)

file2_amplitudes = []
file2_phases = []
with open('Task_4/Outputs/frequency_components_rounded.txt', 'r') as file:
    for line in file:
        data = line.strip().split()
        if len(data) >= 2:
            amplitude, phase = data
            amplitude = round(float(amplitude[:-1]) if amplitude.endswith('f') else float(amplitude), 14)
            phase = float(phase[:-1]) if phase.endswith('f') else float(phase)
            file2_amplitudes.append(amplitude)
            file2_phases.append(phase)

amplitude_comparison = SignalComapreAmplitude(file1_amplitudes, file2_amplitudes)
phase_comparison = SignalComaprePhaseShift(file1_phases, file2_phases)

if amplitude_comparison and phase_comparison:
    print("Amplitude and Phase values match in the two files.")
else:
    print("Amplitude and/or Phase values don't match in the two files.")

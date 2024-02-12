import numpy as np
import math
from CompareSignal import Compare_Signals


def calculate_correlation(signal1, signal2, float_point):
    N = len(signal1)
    result = []

    x1_square = [i ** 2 for i in signal1]
    x2_square = [i ** 2 for i in signal2]
    p12_denominator = math.sqrt((sum(x1_square) * sum(x2_square))) / N
    p12_denominator = round(p12_denominator, float_point)

    # from r1 to r_end
    for i in range(1, N + 1):
        signal2_shifted = np.concatenate((signal2[i:], signal2[:i]))  # Correct circular shifting
        r = round(np.sum(signal1 * signal2_shifted) / N, float_point)
        p = round(r / p12_denominator, float_point)
        result.append(p)

    # r0 == r_end
    result = [result[N - 1]] + result
    indices = list(range(N))
    return indices, result[:N]

def read_file(file):
    indices = []
    samples = []

    with open(file, 'r') as f1:
        for _ in range(3):  # Skip the first 3 lines
            next(f1)

        for line in f1:
            if not line.strip():
                break

            V1, V2 = map(float, line.split())
            indices.append(V1)
            samples.append(V2)

    return np.array(indices), np.array(samples)

def correlate_signals(file_path1, file_path2):
    indices1, samples1 = read_file(file_path1)
    indices2, samples2 = read_file(file_path2)

    result_indices, result_samples = calculate_correlation(samples1, samples2, float_point=8)

    print("Output Signal:")
    for index, sample in zip(result_indices, result_samples):
        print(f"{index} {sample:.8f}")

    #Testing
    Compare_Signals('CorrOutput.txt',result_indices, result_samples)


def main():
    # Specify the file paths directly
    file_path1 = "Corr_input signal1.txt"
    file_path2 = "Corr_input signal2.txt"

    print("Selected files:", file_path1, file_path2)

    correlate_signals(file_path1, file_path2)

if __name__ == "__main__":
    main()

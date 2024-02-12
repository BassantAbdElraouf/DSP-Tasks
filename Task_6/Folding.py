#4)Folding a signal.

import numpy as np

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        # Skip the first 3 lines
        for _ in range(3):
            next(file)

        data = np.genfromtxt(file_path, delimiter=' ', skip_header=3, dtype=float)
        indices_values = data[:, 0]
        signal_values = data[:, 1]
        return indices_values, signal_values

def fold_signal(indices_values, signal_values):
    folded_signal = signal_values[::-1]  # Reverse the signal
    return indices_values, folded_signal

def print_indices_samples(indices_values, signal_values, title="Original"):
    print("\n{} signal_values:".format(title))
    print("indices  sample")
    for index, sample in zip(indices_values, signal_values):
        print("{:<7} {:<7}".format(index, sample))

def main():
    file_path = 'input_fold.txt'

    # Read input data from the file
    indices_values, signal_values = read_input_file(file_path)

    # Fold the signal
    folded_indices, folded_signal = fold_signal(indices_values, signal_values)

    # Print original signal
    print_indices_samples(indices_values, signal_values, title="Original")

    # Print folded signal
    print_indices_samples(folded_indices, folded_signal, title="Folded")

    #Testing

if __name__ == "__main__":
    main()

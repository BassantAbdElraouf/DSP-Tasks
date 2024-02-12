#5)Delaying or advancing a folded signal

import numpy as np
from Shift_Fold_Signal import Shift_Fold_Signal

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        data = np.genfromtxt(file_path, delimiter=' ', skip_header=3, dtype=float)
        indices_values = data[:, 0]
        signal_values = data[:, 1]
        return indices_values, signal_values

def fold_signal(indices_values, signal_values):
    folded_signal = signal_values[::-1]  # Reverse the signal
    return indices_values, folded_signal


def delay_advance_signal(indices_values, k):
    delayed_indices = indices_values + k
    print("indices_values", indices_values)
    print("delayed_indices", delayed_indices)
    return delayed_indices



def main():
    file_path = 'input_fold.txt'

    # Read input data from the file
    indices_values, signal_values = read_input_file(file_path)

    folded_indices, folded_signal = fold_signal(indices_values, signal_values)

    k = int(input("\nEnter the number of steps to delay or advance the signal: "))

    # Delay or advance the signal by k steps
    delayed_indices = delay_advance_signal(folded_indices, k)

    if k == 500:
        Shift_Fold_Signal('Output_ShifFoldedby500.txt',delayed_indices,folded_signal)
    elif k == -500:
        Shift_Fold_Signal('Output_ShiftFoldedby-500.txt',delayed_indices,folded_signal)


if __name__ == "__main__":
    main()
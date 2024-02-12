# 3)Delaying or advancing a signal by k steps

import numpy as np
from ConvTest import ConvTest

def delay_advance_signal(indices_values, k):
    delayed_indices = indices_values + k
    return delayed_indices



def print_indices_samples(indices_values, signal_values, title="Original"):
    print("\n{} signal_values:".format(title))
    print("indices  sample")
    for index, sample in zip(indices_values, signal_values):
        print("{:<7} {:<7}".format(index, sample))


def main():
    indices_values = np.array([-2, -1, 0, 1, 2, 3, 4, 5, 6])
    signal_values = np.array([1, 1, -1, 0, 0, 3, 3, 2, 1])

    # Get the delay/advance value (k) from the user
    k = int(input("Enter the number of steps to delay or advance the signal: "))

    # Delay or advance the signal by k steps
    delayed_indices = delay_advance_signal(indices_values, k)

    # Print original signal
    print_indices_samples(indices_values, signal_values, title="Original")

    # Print delayed or advanced indices
    print_indices_samples(delayed_indices, signal_values, title="Delayed or Advanced")

    ConvTest(indices_values, signal_values)

if __name__ == "__main__":
    main()





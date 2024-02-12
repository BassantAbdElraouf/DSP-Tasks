# 1)Smoothing

import numpy as np
from comparesignals import SignalSamplesAreEqual

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(3):
            next(file)

        #data type error
        data = np.genfromtxt(file, delimiter=' ', filling_values=np.nan) 
        # Remove rows with missing signal values
        data = data[~np.isnan(data[:, 1])]  
        indices_values = data[:, 0]
        signal_values = data[:, 1]
        print("\nData signal_values :\n", signal_values)
        return indices_values, signal_values

def moving_average(data, window_size):
    #array filled with ones ...normalization step
    weights = np.ones(window_size) / window_size
    #N-W+1 ... mode='valid' the output contains only valid data
    return np.convolve(data, weights, mode='valid')


def main():
    Test = int(input("Enter the Test num: "))
    if Test == 1:
        file_path = 'MovAvgTest1.txt'
    else:
        file_path = 'MovAvgTest2.txt'

    # Read input data from the file
    indices_values, signal_values = read_input_file(file_path)

    window_size = int(input("Enter the Window Size for moving average: "))
    smoothed_signal = moving_average(signal_values, window_size)
    print("\nSmoothed signal_values :\n", smoothed_signal)
    print("\n")
    if Test == 1:
        SignalSamplesAreEqual('MovAvgTest1.txt', indices_values, signal_values)
    else:
        SignalSamplesAreEqual('MovAvgTest2.txt', indices_values, signal_values)


if __name__ == "__main__":
    main()




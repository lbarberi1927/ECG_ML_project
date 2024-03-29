import numpy as np
import neurokit2 as nk
import pandas as pd

"""
Parameters to play around with:
    method for ecg_peaks
    method for ecg_delineate
"""

def peak_detection(filtered_signal, SAMPLING_RATE = 300):
    """
    Detects PQRST peaks in a filtered signal.

    Parameters
    ----------
    filtered_signal: np.ndarray 
        of size (n_samples, max_length_signal)
        if a sample doesn't contain max_length_signal points. It is expected to be filled up with NaNs

    Returns
    -------
    PQRST_peaks: Dictionary of Dictionaries
        first dictionary contains key id of sample (integer, row_nr)
            inside there are the keys "ECG_P_Peaks", "ECG_Q_Peaks", "ECG_S_Peaks", "ECG_T_Peaks", "ECG_P_Onsets", "ECG_T_Offsets"
            each then contains the indices at which the specific Peak occurs.
            example: {0: {"ECG_P_Peaks": [345, 678,..], "ECG_Q_Peaks": [45, 376,..], ..}, 1:{..}, ..}
    """
    nr_samples, max_length_signal = filtered_signal.shape

    PQRST_peaks = {} #initialize empty dictionary

    for iteration in range(nr_samples): #neurokit only works with vectors and not with matrices
        ecg_signal = filtered_signal[iteration]
        ecg_signal = ecg_signal[~np.isnan(ecg_signal)] #ignore all nans (filling up the row)
        _, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=SAMPLING_RATE, method='promac') #different methods are possible
        __, waves_peak = nk.ecg_delineate(np.pad(ecg_signal, (0,10), 'median'), rpeaks['ECG_R_Peaks'], sampling_rate=SAMPLING_RATE, method='peaks') #different methods are possible
        waves_peak['ECG_R_Peaks'] = rpeaks['ECG_R_Peaks'].tolist()
        PQRST_peaks[iteration] = waves_peak
        if (iteration%100) == 0:
            print(iteration, "/", nr_samples, "iterations done.")

    return PQRST_peaks

filtered_test_data_path = "/Users/leonardobarberi/Desktop/ETH/Semester_1/AML/task2/X_test_filtered.csv"
X_test_filtered = pd.read_csv(filtered_test_data_path)
X_test_filtered = np.array(X_test_filtered)
X_test_peaks = peak_detection(X_test_filtered)
print("done with peak detection")
peaks_path = "/Users/leonardobarberi/Desktop/ETH/Semester_1/AML/task2/X_test_peaks.npy"
np.save("peaks_path.npy", X_test_peaks)
# X_test_peaks.to_csv(peaks_path)
print("saved succesfully")

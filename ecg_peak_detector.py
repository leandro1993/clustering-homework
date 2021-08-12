import numpy as np
from matplotlib import pyplot as plt
import wfdb
import os 

# wfdb.dl_files('mitdb', "mitdata", ["100.hea", "100.dat"])                # Descarga la señal 100
ecg, fields = wfdb.rdsamp(os.path.join("mitdata", "100"), channels=[0])  # Lectura de la señal

w = 150
fs = fields['fs']

def ecg_filter(signal, fs,  window, threshold):
    mean = np.array([signal[x]-np.mean(signal[x:x+window]) for x in range( len(signal))]) #cuello de botella
    # mean = np.convolve(np.ravel(signal), np.ones(window)/window, mode='valid')
    clipped = np.where(mean<threshold, 0, mean)
    # peaks = np.argwhere(clipped>0)
    # peaks = np.argwhere(mean<threshold)
    peaks = (np.diff(np.sign(np.diff(clipped.flatten()))) < 0).nonzero()[0] + 1 # local max
    # qrs = np.array([np.argmax(clipped[i:i+window]) for i in range(len(clipped))])
    return peaks

pk = ecg_filter(ecg, fs, w, 0.35)

length = 10
plt.plot(ecg[:fs*length], c='b')
for i in range(length+1):
    plt.plot(pk[i], ecg[pk[i]],'*',markersize=10)

plt.show()
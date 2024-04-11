import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import datetime
import os
data_folder = '../dataset' # walk + pick + speak
data = os.listdir(data_folder)
def time_read(x):
    return datetime.datetime.strptime(x, ' %H:%M:%S.%f')
for d in data:
    file = os.path.join(data_folder, d, 'data__1.csv')
    df = pd.read_csv(file, header=0, index_col=False, usecols=(0, 3, 4, 5), converters={'时间': time_read})
    # remove the first and last 50 samples
    df = df[50:-50]
    time = [(t - df['时间'][50]).total_seconds() for t in df['时间']]
    fig, axs = plt.subplots(1, 4)
    for i, key in enumerate(df.keys()):
        if key == '时间':
            continue
        axs[0].plot(time, df[key])
        f, t, stft = signal.stft(df[key], fs=200, nperseg=100)
        axs[i].pcolormesh(t, f, np.abs(stft), shading='gouraud')
        axs[i].set_ylim([0, 10])
    plt.show()

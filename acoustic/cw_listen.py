'''
Keep those the parameter same as "generate_wav.py"
processing reference "Earmonitor: In-ear Motion-resilient Acoustic Sensing Using Commodity Earphones"
"APG: Audioplethysmography for Cardiac Monitoring in Hearables"
'''
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np
import os
def run_sensing(file, preamble, freq=20000):
    fs, record = wavfile.read(file)
    record = record / 32767
    record /= np.max(np.abs(record), axis=0, keepdims=True)
    record = record[:, 0]
    b, a = signal.butter(8, [freq-1000, freq+1000], 'bandpass', fs=fs)
    record = signal.filtfilt(b, a, record)

    correlate_record = np.correlate(record[:int(fs * 1)], preamble)
    delay_record = np.argmax(correlate_record)
    record = record[delay_record + len(preamble):]
    t = np.linspace(0, len(record)/fs, len(record))
    in_reference = np.sin(2 * np.pi * freq * t)
    quadrature_reference = np.sin(2 * np.pi * freq * t + np.pi/2)
    b, a = signal.butter(4, 20, 'lowpass', fs=fs)
    I = record * in_reference
    Q = record * quadrature_reference
    I = signal.filtfilt(b, a, I)
    Q = signal.filtfilt(b, a, Q)
    
    down_sample = 48
    R = ((I**2 + Q**2)**0.5)[::down_sample]
    phi = np.arctan2(Q, I)[::down_sample]
    # b, a = signal.butter(4, [0.6, 2.5], 'bandpass', fs=fs/down_sample)
    # R = signal.filtfilt(b, a, R)
    # phi = signal.filtfilt(b, a, phi)
    len_fft = len(R)//2
    fft_R = np.fft.fft(R)[:len_fft]
    fft_phi = np.fft.fft(phi)[:len(R)//2]
    fft_freq = fs * np.fft.fftfreq(len(R))[:len(R)//2]

    fig, axs = plt.subplots(6, 1)
    axs[0].plot(record)
    #axs[1].specgram(record[:fs], NFFT=1024, Fs=fs, noverlap=512)
    axs[1].plot(I)
    axs[1].plot(Q)
    axs[2].plot(R)
    axs[3].plot(phi)
    axs[4].plot(fft_freq, np.abs(fft_R))
    axs[5].plot(fft_freq, np.abs(fft_phi))

    plt.show()
    return
def run():
    folder = 'CW_sensing'
    files = os.listdir(folder)
    files.remove('transmited.wav')
    files.remove('preamble.wav')
    fs, preamble = wavfile.read(folder + '/preamble.wav')
    preamble = preamble / 32767
    for file in files:
        center_freq = int(file.split('_')[0])
        print('Center frequency: ', center_freq, 'filename: ', file)
        run_sensing(folder + '/' + file, preamble, center_freq)
        # break

if __name__ == '__main__':
    run()
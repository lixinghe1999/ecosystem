'''
Keep those the same as "generate_wav.py"
'''
total_duration = 10  # Total duration of the signal in seconds
pulse_duration = 0.02  # Duration of each pulse in seconds
pulse_interval = 0.0  # Time interval between pulses in seconds
sample_rate = 48000  # Sample rate in Hz
start_freq = 18000  # Starting frequency in Hz
end_freq = 22000  # Ending frequency in Hz

vs = 340
period = int(sample_rate * (pulse_duration + pulse_interval))
chirp_len = int(sample_rate * pulse_duration)
bandwidth = end_freq - start_freq
dist_min = 0.2
dist_max = 0.5
range_fft_size = int(10 * sample_rate * pulse_duration)
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

def load_mic(fname):
    rate, data = wavfile.read(fname)
    assert rate == sample_rate
    data = data / 32767  
    return data
    

def process_mic(data):
    ref = signal.chirp(np.linspace(0, pulse_duration, chirp_len), start_freq, pulse_duration, end_freq)
    low_freq = dist_min * 2 / vs / pulse_duration * bandwidth
    high_freq = dist_max * 2 / vs / pulse_duration * bandwidth
    b, a = signal.butter(5, [low_freq, high_freq], 'bandpass', fs=sample_rate)
    h = signal.firwin(300, [low_freq, high_freq], pass_zero=False, fs=sample_rate)
    range_search = np.linspace(0, sample_rate//2, range_fft_size//2) * vs * pulse_duration/ 2 / bandwidth
    range_index = np.logical_and(range_search > dist_min, range_search < dist_max)
    range_search = range_search[range_index]

    fig, axs = plt.subplots(4, 1)
    range_ffts = []

    for i in range(0, len(data) // int(total_duration * sample_rate)+1):
        data_chunk = data[i * int(total_duration * sample_rate): (i+1) * int(total_duration * sample_rate)]

        correlation = np.correlate(data_chunk, ref, "valid")
        delay = np.argmax(correlation)
        max_frame = (int(total_duration * sample_rate) - delay)//period -1 
        receive_signal = data_chunk[delay: delay + chirp_len]
        mix_signal = receive_signal * ref
        mix_signal = signal.lfilter(h, 1, mix_signal)
        # receive_signal2 = data_chunk[delay+period: delay+period + chirp_len]
        # mix_signal2 = receive_signal2 * ref
        # mix_signal2 = signal.lfilter(h, 1, mix_signal2)
        # mix_signal = mix_signal - mix_signal2

        range_fft = np.fft.fft(mix_signal, range_fft_size)[:range_fft_size//2]
        range_fft_ref = np.abs(range_fft[range_index])**2/range_fft_size
        peak_index = np.argmax(range_fft_ref)
        axs[0].plot(mix_signal)
        axs[1].plot(range_search, range_fft_ref)
        for j in range(max_frame):
            receive_signal = data_chunk[delay: delay + chirp_len]
            mix_signal = receive_signal * ref
            mix_signal = signal.lfilter(h, 1, mix_signal)

            # receive_signal2 = data_chunk[delay+period: delay+period + chirp_len]
            # mix_signal2 = receive_signal2 * ref
            # mix_signal2 = signal.lfilter(h, 1, mix_signal2)
            # mix_signal = mix_signal - mix_signal2

            range_fft = np.fft.fft(mix_signal, range_fft_size)[:range_fft_size//2]
            range_fft = np.abs(range_fft[range_index])**2/range_fft_size
            range_ffts.append(range_fft[peak_index])
            axs[2].plot(range_search, range_fft-range_fft_ref)

            delay += period
        axs[3].plot(range_ffts)
    plt.show()
    range_ffts = np.array(range_ffts)
    return range_ffts
def show_mic(data):
    
    return
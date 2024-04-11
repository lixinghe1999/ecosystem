import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
def fmcw(preamble_duration = 0.4, total_duration = 10, pulse_duration = 0.05, pulse_interval = 0.0, sample_rate = 48000,
         start_freq = 16000 , end_freq = 21000):
    window = signal.windows.tukey(int(pulse_duration * sample_rate), 0.2, )
    num_pulses = int(total_duration / (pulse_duration + pulse_interval))
    data = np.zeros(int(total_duration * sample_rate))
    pulse_time = 0
    for _ in range(num_pulses):
        # Generate the FMCW pulse signal
        t = np.linspace(0, pulse_duration, int(pulse_duration * sample_rate), endpoint=False)
        pulse_signal = signal.chirp(t, start_freq, pulse_duration, end_freq)
        pulse_signal = pulse_signal * window
        # Add the pulse signal to the main signal
        data[int(pulse_time * sample_rate): int(pulse_time * sample_rate)+int(pulse_duration * sample_rate) ] += pulse_signal
        # Update the pulse time for the next pulse
        pulse_time += pulse_duration + pulse_interval
    preamble = signal.chirp(np.linspace(0, preamble_duration/2, int(preamble_duration/2 * sample_rate), endpoint=False), start_freq, preamble_duration, end_freq)
    window = signal.windows.tukey(int(preamble_duration/2 * sample_rate), 0.2, )
    preamble = preamble * window
    preamble = np.pad(preamble, (len(preamble)//2, len(preamble)//2), 'constant')
    data = (data * 32767).astype(np.int16)
    preamble = (preamble * 32767).astype(np.int16)
    data = np.concatenate((preamble, data))
    return data, preamble
def cw(preamble_duration = 0.4, total_duration = 10, sample_rate = 48000, freq = 20000, start_freq = 16000 , end_freq = 21000):
    t = np.linspace(0, total_duration, int(total_duration * sample_rate), endpoint=False)
    data = np.sin(2 * np.pi * freq * t)
    preamble = signal.chirp(np.linspace(0, preamble_duration/2, int(preamble_duration/2 * sample_rate), endpoint=False), start_freq, preamble_duration, end_freq)
    window = signal.windows.tukey(int(preamble_duration/2 * sample_rate), 0.2, )
    preamble = preamble * window
    preamble = np.pad(preamble, (len(preamble)//2, len(preamble)//2), 'constant')
    data = (data * 32767).astype(np.int16)
    preamble = (preamble * 32767).astype(np.int16)
    data = np.concatenate((preamble, data))
    return data, preamble

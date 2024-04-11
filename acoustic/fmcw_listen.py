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
pulse_duration = 0.05  # Duration of each pulse in seconds
pulse_interval = 0.0  # Time interval between pulses in seconds
sample_rate = 48000  # Sample rate in Hz
start_freq = 16000  # Starting frequency in Hz
end_freq = 21000  # Ending frequency in Hz
dist_fft_size = 8192 # int(pulse_duration * sample_rate)
dist_max = 0.0005 
def run_sensing(file, reference, preamble):
    fs, record = wavfile.read(file)
    record = record / 32767
    record /= np.max(np.abs(record), axis=0, keepdims=True)
    record_raw = record.copy()
    reference = reference[:, 0]
    record = record[:, 0]
    b, a = signal.butter(4, 16000, 'highpass', fs=fs)
    reference = signal.filtfilt(b, a, reference)
    record = signal.filtfilt(b, a, record)

    correlate_reference = np.correlate(reference[:int(fs * 1)], preamble)
    correlate_record = np.correlate(record[:int(fs * 1)], preamble)
    delay_reference = np.argmax(correlate_reference)
    delay_record = np.argmax(correlate_record)
    reference = reference[delay_reference + len(preamble):]
    record = record[delay_record + len(preamble):]
    record_raw = record_raw[delay_record + len(preamble):]

    fig, axs = plt.subplots(6, 1)
    axs[0].plot(reference[:int(fs * 1)]+1)
    axs[0].plot(record[:int(fs * 1)]-1)

    chirp = signal.chirp(np.arange(0, 0.05, 1/fs), 16000, 0.05, 21000)
    freq_max = dist_max*2/340/pulse_duration*(end_freq - start_freq)
    b, a = signal.butter(4, freq_max, 'lowpass', fs=fs) 

    # dist = (fs * np.fft.fftfreq(dist_fft_size)*340*pulse_duration/(2*(end_freq - start_freq)))[:dist_fft_size//2]
    dist = (fs * np.fft.fftfreq(dist_fft_size)*pulse_duration/(end_freq - start_freq))[:dist_fft_size//2]
    dist_select = dist < dist_max
    num_pulse = int(len(record) / (pulse_duration * fs))
    phase_list = []
    for i in range(num_pulse-1):
        # mix_reference = reference[i*int(fs * 0.05):(i+1)*int(fs * 0.05)] * chirp
        mix_reference = record[i*int(fs * 0.05):(i+1)*int(fs * 0.05)] * chirp
        mix_record = record[(i+1)*int(fs * 0.05):(i+2)*int(fs * 0.05)] * chirp
        mix_reference = signal.filtfilt(b, a, mix_reference)
        mix_record = signal.filtfilt(b, a, mix_record)
        mix = mix_record - mix_reference


        fft_mix_reference = np.fft.fft(mix_reference, n=dist_fft_size)[:dist_fft_size//2]
        fft_mix_reference = fft_mix_reference / np.max(np.abs(fft_mix_reference))
        
        fft_mix_record = np.fft.fft(mix_record, n=dist_fft_size)[:dist_fft_size//2]
        fft_mix_record = fft_mix_record / np.max(np.abs(fft_mix_record))

        fft_mix = np.fft.fft(mix, n=dist_fft_size)[:dist_fft_size//2]
        fft_mix = fft_mix / np.max(np.abs(fft_mix))
        fft_phase = np.angle(fft_mix)[dist_select]
        phase_list.append(fft_phase)

        axs[1].plot(dist[dist_select], np.abs(fft_mix_reference)[dist_select], color='r')
        axs[1].plot(dist[dist_select], np.abs(fft_mix_record)[dist_select], color='b')

        axs[2].plot(dist[dist_select], np.abs(fft_mix)[dist_select])
        # axs[2].plot(dist[dist_select], np.abs(fft_mix)[dist_select], color='r')
    
    record_raw = record_raw[::48, :]
    record_raw = record_raw[:5000, :]
    b_listen, a_listen = signal.butter(4, [0.8, 2.5], 'bandpass', fs=1000)
    listen_record = signal.filtfilt(b_listen, a_listen, record_raw, axis=0)
    # fft_listen = np.fft.fft(listen_record[:, 0], n=5000)[:2500]
    # fft_peak = np.argmax(np.abs(fft_listen))
    # fft_freq = np.fft.fftfreq(5000, 1/1000)[:2500]
    # print(fft_freq[fft_peak])
    axs[3].plot(listen_record[:, 0])
    #axs[3].plot(peak1, listen_record[peak1, 0], 'x')

    phase_list = np.array(phase_list)
    phase_list = np.unwrap(phase_list)
    # convert phase to mm
    phase_list = phase_list / (0.02 * np.pi) / 10
    select_bin = np.argmax(np.std(phase_list, axis=0))
    phase_list = phase_list[:, select_bin]
    t = np.arange(0, len(phase_list), 1) * pulse_duration
    b, a = signal.butter(4, [0.8, 2.5], 'bandpass', fs=1/pulse_duration)
    phase_list = signal.filtfilt(b, a, phase_list, axis=0)

    from vmdpy import VMD  
    alpha = 2000       # moderate bandwidth constraint  
    tau = 0.            # noise-tolerance (no strict fidelity enforcement)  
    K = 3              # 3 modes  
    DC = 0             # no DC part imposed  
    init = 1           # initialize omegas uniformly  
    tol = 1e-7  
    #. Run actual VMD code  
    u, u_hat, omega = VMD(phase_list, alpha, tau, K, DC, init, tol)  
    axs[4].plot(t, u.T)
    for decomposed in u:
        fft_phase = np.fft.fft(decomposed)[:len(phase_list)//2]
        freq_phase = np.fft.fftfreq(len(phase_list), pulse_duration)[:len(phase_list)//2]
        max_freq = freq_phase[np.argmax(np.abs(fft_phase))]
        print(max_freq)
        phase_list -= decomposed
    axs[5].plot(t, phase_list)
    plt.show()
    return
def run():
    folder = 'FMCW_sensing'
    files = os.listdir(folder)
    files.remove('transmited.wav')
    files.remove('preamble.wav')
    files.remove('reference.wav')
    fs, reference = wavfile.read(folder + '/reference.wav' )
    fs, preamble = wavfile.read(folder + '/preamble.wav')
    reference = reference / 32767
    reference /= np.max(np.abs(reference), axis=0, keepdims=True)
    preamble = preamble / 32767
    for file in files:
        run_sensing(folder + '/' + file, reference, preamble)

if __name__ == '__main__':
    run()
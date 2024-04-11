import sounddevice as sd
import scipy.io.wavfile as wavfile
import os
import time
from generate_wav import fmcw, cw
import argparse

args = argparse.ArgumentParser()
args.add_argument('--reference',default=False, required=False, action='store_true',help='Record reference')
args.add_argument('--fmcw',default=False, required=False, action='store_true', help='turn on fmcw mode')
args = args.parse_args()

if args.fmcw:
    file = 'FMCW_sensing.wav'
    data, preamble = fmcw()

    file = 'FMCW_identification.wav'
    data, preamble = fmcw(pulse_interval = 0.15, start_freq = 1000,  end_freq = 21000)
    folder = file[:-4]
    os.makedirs(folder, exist_ok=True)
    wavfile.write(os.path.join(folder, 'transmited.wav'), 48000, data) # save transmited data
    wavfile.write(os.path.join(folder, 'preamble.wav'), 48000, preamble) # save transmited data
    myrecording = sd.playrec(data, samplerate=48000, channels=2, blocking=True)

    if args.reference:
        file = os.path.join(folder, 'reference.wav')
        wavfile.write(file, 48000, myrecording)
    else:
        time_stamp = time.strftime("%H%M%S")
        file = os.path.join(folder, time_stamp + '.wav')
        wavfile.write(file, 48000, myrecording)
else:
    file = 'CW_sensing.wav'
    freq = 22000
    data, preamble = cw(freq=freq)
    folder = file[:-4]
    os.makedirs(folder, exist_ok=True)
    wavfile.write(os.path.join(folder, 'transmited.wav'), 48000, data) # save transmited data
    wavfile.write(os.path.join(folder, 'preamble.wav'), 48000, preamble) # save transmited data
    myrecording = sd.playrec(data, samplerate=48000, channels=2, blocking=True)
    time_stamp = time.strftime("%H%M%S")
    file = os.path.join(folder, str(freq) + '_' + time_stamp + '.wav')
    wavfile.write(file, 48000, myrecording)



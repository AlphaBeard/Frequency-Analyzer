import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import itertools
import csv
import collections

FILENAME = "dial_tone.wav"
NOTES_FILENAME = "notes.csv"


def load_notes_dict():
    notes_dict = collections.defaultdict(list)
    with open(NOTES_FILENAME, 'r') as data:
        for note_dict in csv.DictReader(data):
            for k, v in note_dict.items():
                notes_dict[k].append(v)
    return notes_dict

def get_amplitudes_from_sound_file(sound_file):
    info = sf.info(FILENAME)
    sampling_interval = 1/info.samplerate

    rms = np.array([np.sqrt(np.mean(block**2)) for block in
                    sf.blocks(FILENAME, blocksize=1024, overlap=0)])
    raw_values = list(itertools.chain.from_iterable([block for block in
                                                    sf.blocks(FILENAME, blocksize=1024, overlap=0)]))
    t = np.array(range(len(rms)))*(1024/sampling_interval)

def get_fourier_data(amplitude_data):
    info = sf.info(FILENAME)
    # Frequency domain representation
    fourier_transform = np.fft.fft(
        amplitude_data)/len(amplitude_data)  # Normalize amplitude
    fourier_transform = fourier_transform[range(
        int(len(amplitude_data)/2))]  # Exclude sampling frequency

    tpCount = len(amplitude_data)
    values = np.arange(int(tpCount/2))
    timePeriod = info.duration
    frequencies = values/timePeriod
    return frequencies, abs(fourier_transform)

def calculate_component_frequncies(frequencies, fourier_transform, fs_threshold=.1):
    component_frequencies = [f for f, amp in zip(
    frequencies, abs(fourier_transform)) if amp > fs_threshold]
    return component_frequencies

# Frequency domain representation
# fig = plt.figure(figsize=[15, 15])
# ax1, ax2, *_ = fig.subplots(2)
# ax1.plot(t, np.array(rms))
# ax2.set_title('Fourier transform depicting the frequency components')
# ax2.plot(frequencies, abs(fourierTransform))
# ax2.set_xlabel('Frequency')
# ax2.set_ylabel('Amplitude')
# plt.show()
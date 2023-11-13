from Nsound import *
from pydub import AudioSegment
import os
import sys

if len(sys.argv) <= 1:
    os.system("echo Usage: python gavin_nsound_pydub.py [hz of base note]")
    sys.exit(-1)

sr = 44100.0
BITS_PER_SAMPLE = 24

def stereo_note(sr, duration, f1, f2, gaussian_width):

    sin = Sine(sr)

    audio = AudioStream(sr, 2)

    envelope = sin.drawFatGaussian(duration, gaussian_width)

    audio[0] = sin.generate(duration, f1)
    audio[1] = sin.generate(duration, f2)

    return audio * envelope

def mono_note(sr, duration, f1, gaussian_width):

    sin = Sine(sr)

    audio = AudioStream(sr, 1)

    envelope = sin.drawFatGaussian(duration, gaussian_width)

    audio[0] = sin.generate(duration, f1)

    return audio * envelope

def chord(sr, base_frequency, duration, gaussian_width, name):

    name1 = "1" + name
    name2 = "2" + name

    sine = Sine(sr)

    out1 = AudioStream(sr, 2)

    out1 << stereo_note(sr, duration, base_frequency, (base_frequency * 5 / 4), gaussian_width) \
        << sine.silence(0.5)

    out1 >> name1

    out2 = AudioStream(sr, 1)

    out2 << mono_note(sr, duration, (base_frequency * 3 / 2), gaussian_width)
    out2 << sine.silence(0.5)

    out2 >> name2

    sound1 = AudioSegment.from_file(name1, format="wav")
    sound2 = AudioSegment.from_file(name2, format="wav")

    sound1 = sound1 - 7
    sound2 = sound2 - 7

    combined = sound1.overlay(sound2)

    file_handle = combined.export(name, format="wav")
    os.remove(name1)
    os.remove(name2)

chord(sr, float(sys.argv[1]), 1.0, .90, "gavin_test_chord_" + sys.argv[1] + ".wav")
sys.exit()
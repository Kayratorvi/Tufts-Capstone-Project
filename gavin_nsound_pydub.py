from Nsound import *
from pydub import AudioSegment

sr = 44100.0
BITS_PER_SAMPLE = 24

def chord(sr, duration, f1, f2, gaussian_width):

    sin = Sine(sr)

    audio = AudioStream(sr, 2)

    envelope = sin.drawFatGaussian(duration, gaussian_width)

    audio[0] = sin.generate(duration, f1)
    audio[1] = sin.generate(duration, f2)

    return audio * envelope

def note(sr, duration, f1, gaussian_width):

    sin = Sine(sr)

    audio = AudioStream(sr, 1)

    envelope = sin.drawFatGaussian(duration, gaussian_width)

    audio[0] = sin.generate(duration, f1)

    return audio * envelope

sine = Sine(sr)

c = 258

out1 = AudioStream(sr, 2)

out1 << chord(sr, 0.75, c, (c * 5 / 4), 0.90) \
    << sine.silence(0.5)

out1 >> "gavin_nsound_ji1.wav"

out2 = AudioStream(sr, 1)

out2 << note(sr, 0.75, (c * 3 / 2), 0.90)
out2 << sine.silence(0.5)

out2 >> "gavin_nsound_ji2.wav"

sound1 = AudioSegment.from_file("./gavin_nsound_ji1.wav", format="wav")
sound2 = AudioSegment.from_file("./gavin_nsound_ji2.wav", format="wav")

sound1 = sound1 - 7
sound2 = sound2 - 7

combined = sound1.overlay(sound2)

file_handle = combined.export("./gavin_nsound_ji3.wav", format="wav")
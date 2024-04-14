from Nsound import *
from pydub import AudioSegment
import os

class AudioChannels:
    def __init__(self, sr=96000.0):
        self.audio = list()
        self.timestamps = list()
        self.sin = Sine(sr)
        self.sr = sr
        self.note_letters = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
        self.note_frequencies = [261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305, 440.0, 466.164, 493.883]
        self.intervals = [1 / 1, 16 / 15, 9 / 8, 6 / 5, 5 / 4, 4 / 3, 45 / 32, 3 / 2, 8 / 5, 5 / 3, 9 / 5, 15 / 8]

    def audio_note(self, freq, duration, gaussian_width=0.80):
        audio = AudioStream(self.sr)
        envelope = self.sin.drawFatGaussian(duration, gaussian_width)
        audio[0] = self.sin.generate(duration, freq)

        return audio * envelope

    def add_silence(self, index, duration):
        if duration > 0.0:
            self.audio[index] << self.sin.silence(duration)
            self.timestamps[index] += duration

    def add_note(self, note):
        added = False
        for i, time in enumerate(self.timestamps):
            if time <= note.timestamp_in_seconds and not added:
                self.add_silence(i, note.timestamp_in_seconds - time)
                self.audio[i] << self.audio_note(self.get_frequency(note), note.duration_seconds)
                self.timestamps[i] += note.duration_seconds
                added = True
        
        if not added:
            self.audio.append(AudioStream(self.sr))
            self.timestamps.append(0.0)
            i = len(self.audio) - 1
            
            self.add_silence(i, note.timestamp_in_seconds)
            self.audio[i] << self.audio_note(self.get_frequency(note), note.duration_seconds)
            self.timestamps[i] += note.duration_seconds
            added = True
        
        return

    def note_dist(self, root, note):
        if root == -1:
            return 0
        
        dist = (note % 12) - (root % 12)

        if dist >= 0:
            return dist
        else:
            return ((note % 12) + 12) - (root % 12)

    def get_frequency(self, note):
        note_num = note.note % 12
        octave_diff = (note.note // 12) - 5
        octave_diff -= (note_num) < note.bass_tuning
        interval_from_bass = self.note_dist(note.bass_tuning, note_num) 

        if note.bass_tuning == -1:
            freq = self.note_frequencies[note_num]
        else:
            freq = self.note_frequencies[note.bass_tuning] * self.intervals[interval_from_bass]
        
        return self.change_octave(freq, octave_diff)
    
    def change_octave(self, freq, octave_diff):
        while octave_diff != 0:
            if octave_diff < 0:
                freq = freq / 2
                octave_diff += 1
            else: 
                freq = freq * 2
                octave_diff -= 1
        
        return freq

    def output_audio(self, name):
        print("Starting to output audio.\n")
        for i, channel in enumerate(self.audio):
            channel >> "channel_" + str(i) + ".wav"
            if (not os.path.exists("channel_" + str(i) + ".wav")):
                print("FAILED TO EXPORT CHANNEL " + str(i) + "\n")

        combined = AudioSegment.from_file("channel_0.wav", format="wav")
        combined = combined - 24

        for i in range(1, len(self.audio)):
            chan0 = combined
            tempFileName = "channel_" + str(i) + ".wav"
            chan1 = AudioSegment.from_file(tempFileName, format="wav")
            chan1 = chan1 - 24
            combined = chan0.overlay(chan1)
            os.remove(tempFileName)

        file_handle = combined.export(name, format="wav")
        os.remove("channel_0.wav")
        print("Finished output file >> "+ name + "\n")
        return
        
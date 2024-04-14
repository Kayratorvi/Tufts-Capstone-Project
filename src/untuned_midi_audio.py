from Nsound import *
from pydub import AudioSegment
from mido import MidiFile
from midi_preprocessing import *
import os
import sys

if len(sys.argv) <= 1:
    os.system("echo Usage: python midi_parser.py midi_file_name")
    sys.exit(-1)

mid = MidiFile(sys.argv[1])
mergedMid = mid.merged_track
notes = process_note_lengths(mergedMid, mid.ticks_per_beat)

if len(sys.argv) <= 2:
    output_wav(notes, "output.wav")
else:
    output_wav(notes, sys.argv[2])
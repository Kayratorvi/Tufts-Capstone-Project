from Nsound import *
from pydub import AudioSegment
from mido import MidiFile
from midi_preprocessing import link_notes, process_note_lengths
import os
import sys
        
if len(sys.argv) <= 1:
    os.system("echo Usage: python midi_parser.py midi_file_name")
    sys.exit(-1)

mid = MidiFile(sys.argv[1])
mergedMid = mid.merged_track

#print(mergedMid)
#print("**********************\n**********************")
queue = process_note_lengths(mergedMid)
print(queue)
link_notes(queue, mid.ticks_per_beat - 1)
print(queue[38])
print(mid.ticks_per_beat)
print(queue[38].linked_notes)
print(queue[38].linked_indices)
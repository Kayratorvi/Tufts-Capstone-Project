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

#print(mergedMid)
#print("**********************\n**********************")
queue = process_note_lengths(mergedMid, mid.ticks_per_beat)
#print(queue)
link_notes(queue, mid.ticks_per_beat - 1)
tune_all_notes(queue)
i = 37
#print(queue)
"""
print(queue[i])
print(mid.ticks_per_beat)
print("Linked notes: " + str(queue[i].linked_notes))
print(queue[i].unique_linked_notes())
"""
output_wav(queue, "output.wav")
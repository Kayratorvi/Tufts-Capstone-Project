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
queue = process_note_lengths(mergedMid)
#print(queue)
link_notes(queue, mid.ticks_per_beat - 1)
tune_all_notes(queue)
i = 38
print(queue)
#print(mid.ticks_per_beat)
#print("Linked notes: " + str(queue[i].linked_notes))
#print(queue[i].unique_linked_notes())
#print("\nRelated notes: " + str(queue[i].nearby_notes))
#print(queue[i].unique_nearby_notes())                          
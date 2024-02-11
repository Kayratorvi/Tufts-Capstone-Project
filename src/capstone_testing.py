from Nsound import *
from pydub import AudioSegment
from mido import MidiFile
from mymidimessage import MidiMessageExt
import os
import sys

if len(sys.argv) <= 1:
    os.system("echo Usage: python midi_parser.py midi_file_name")
    sys.exit(-1)

mid = MidiFile(sys.argv[1])
mergedMid = mid.merged_track
#print(mid.ticks_per_beat)
#print(mergedMid)
#print(mergedMid[1000])
#print(mergedMid[1000].channel)
#print(mergedMid[1000].type)
#print(mergedMid[1000].velocity)
#print(mergedMid[1000].time)
#print(mergedMid[0].is_meta)

queue = list()
totalDeltaTime = 0

for message in mergedMid:
    foundNote = False
    totalDeltaTime += message.time
    if not message.is_meta:
        if message.type == "note_on" and message.velocity != 0:
            queue.append(MidiMessageExt(message.channel, message.note, message.velocity, message.time, totalDeltaTime))

        elif (message.type == "note_on" and message.velocity == 0) or message.type == "note_off":
            for note in queue:
                if note.note == message.note and note.channel == message.channel and note.note_length < 0:
                    foundNote = True
                    note.change_note_length(totalDeltaTime - note.timestamp)
                    break
            
            if not foundNote:
                raise RuntimeError("Couldn't find the note to match note_off message.")
        
        else:
            print("Didn't process this message: " + str(message))

print(queue)


# Tentative MIDI Parsing Plan:
# Add MIDI messages to queue separated by beat (MidiFile.ticks_per_beat)
# When a beat has past before the next message is to be added, 
# analyze the messages currently in the queue to determine tuning,
# and use that tuning when feeding the messages in queue to NSound.
# Empty the queue before adding the next messages. 

# When taking in messages from the queue, add them to another queue-like 
# structure that awaits a note_off message or a note_on message that
# matches the message in all attributes except having a velocity of 0.

# 2/2/24 Update
# Read in MIDI file message by message and modify each note_on message to include the note_off timestamp. Basically, each note_on message needs to be stored into memory with a timestamp until a note_off or note_on with velocity 0 message is found. Then, the original note_on message is modified to include exactly how much time that note is on. This will require deviating from the MIDI message structure and using my own data structure entirely. 
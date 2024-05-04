from midimessageext import MidiMessageExt
from audio_channels import AudioChannels
from Nsound import *
from pydub import AudioSegment
import os

log = open("log.txt", "w")

def process_note_lengths(midi, ticks_per_beat):
    print("Reading MIDI File...\n")
    queue = list()
    totalDeltaTime = 0
    totalTimeInSecs = 0.0
    index = -1
    tempo = 500000

    for message in midi:
        index = index + 1
        foundNote = False
        totalDeltaTime += message.time
        if not message.is_meta:
            totalTimeInSecs += (float(message.time) / ticks_per_beat) * (tempo / 1000000.0)

            if message.type == "note_on" and message.velocity != 0:
                queue.append(MidiMessageExt(message.channel, message.note, message.velocity, totalDeltaTime, tempo, ticks_per_beat, totalTimeInSecs))

            elif (message.type == "note_on" and message.velocity == 0) or message.type == "note_off":
                for note in queue:
                    if note.note == message.note and note.channel == message.channel and note.note_length < 0:
                        foundNote = True
                        note.change_note_length(totalDeltaTime - note.timestamp)
                        note.set_duration_seconds()
                        break
                
                if not foundNote:
                    raise RuntimeError("Couldn't find the note to match note_off message.")
            
            else:
                log.write("\nDidn't process this message: " + str(message))
        elif message.type == "set_tempo":
            tempo = message.tempo
            log.write("\nTempo meta_message: " + str(message))
            totalTimeInSecs += (float(message.time) / ticks_per_beat) * (tempo / 1000000.0)

    return queue

def link_notes(notes, ticks_per_beat):
    # This loop adds notes that end within one beat or after the current note
    for i, note in enumerate(notes):
        note.set_index(i)
        for to_link_index in range(i - 1, -1, -1):
            if notes[to_link_index].note_ends_timestamp() > (note.timestamp - ticks_per_beat):
                # note is being played within one beat earlier of current note
                note.link_note(notes[to_link_index])
            else:
                break # there may be notes that start much earlier but have a long duration, will consider in next loop section

        # This loop handles any note that starts much earlier in 
        # the music and has an exceptionally long duration that 
        # extends much longer than notes that start after this note 
        # but before the note in the linking step. These notes will 
        # already be added in previous notes and will be added by
        # looking at the linked notes of all currently linked notes
        for linked_note in note.linked_notes:
            for linked_note_linked_note in linked_note.linked_notes:
                if (linked_note_linked_note.note_ends_timestamp() > (note.timestamp - ticks_per_beat)) and linked_note_linked_note not in note.linked_notes:
                    note.link_note(linked_note_linked_note)
                            
    # This loop adds all notes that start within one beat after the current note
    for i, note in enumerate(notes):
        for to_link_index2 in range(i + 1, len(notes), 1):
            if notes[to_link_index2].timestamp < (note.timestamp + ticks_per_beat):
                # note begins within one beat later of current note
                note.link_note(notes[to_link_index2])
            else:
                break # all other notes begin later in music
        
        note.separate_notes_by_concurrency()

def tune_all_notes(notes):
    print("Performing chord analysis...\n")
    for i, note in enumerate(notes):
        note.set_tuning(notes)

def output_wav(notes, name):
    audio = AudioChannels()

    print("Starting to add notes to NSound stream...\n")

    for note in notes:
        audio.add_note(note)

    print("Finished adding notes to NSound stream.\n")
    
    audio.output_audio(name)

class MidiMessageExt:
    def __init__(self, channel, note, velocity, timestamp):
        self.channel = channel
        self.note = note
        self.velocity = velocity
        self.timestamp = timestamp
        self.note_length = -1 
        self.frequency = -1.0 
        self.duration_seconds = -1.0 
        self.linked_notes = list()
        self.linked_indices = list()

    def __repr__(self):
        return f"\nMidiMessageExt(channel={self.channel}, note={self.note}, velocity={self.velocity}, timestamp={self.timestamp}, note_length={self.note_length}, tuning={self.frequency}, duration_seconds={self.duration_seconds})"

    def __str__(self):
        return f"\nMidiMessageExt(channel={self.channel}, note={self.note}, velocity={self.velocity}, timestamp={self.timestamp}, note_length={self.note_length}, tuning={self.frequency}, duration_in_seconds={self.duration_seconds})"

    def change_frequency(self, frequency):
        self.frequency = frequency

    def change_note_length(self, note_length):
        self.note_length = note_length

    def calc_duration_seconds(self, tempo, ticks_per_beat):
        self.duration_seconds = (float(self.note_length) / ticks_per_beat) * (tempo / 1000000.0)
        return self.duration_seconds
    
    def link_note(self, note, index):
        self.linked_notes.append(note)
        self.linked_indices.append(index)

    def note_ends_timestamp(self):
        return self.timestamp + self.note_length
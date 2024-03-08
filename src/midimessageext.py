class MidiMessageExt:
    def __init__(self, channel, note, velocity, timestamp):
        self.channel = channel
        self.note = note
        self.velocity = velocity
        self.timestamp = timestamp
        self.i = -1
        self.note_length = -1 
        self.frequency = -1.0 
        self.duration_seconds = -1.0 
        self.linked_notes = list()
        self.nearby_notes = list()

    def __repr__(self):
        return f"\nMidiMessageExt(channel={self.channel}, note={self.note}, velocity={self.velocity}, timestamp={self.timestamp}, note_length={self.note_length}, tuning={self.frequency}, duration_seconds={self.duration_seconds}, index={self.i})"

    def __str__(self):
        return f"\nMidiMessageExt(channel={self.channel}, note={self.note}, velocity={self.velocity}, timestamp={self.timestamp}, note_length={self.note_length}, tuning={self.frequency}, duration_in_seconds={self.duration_seconds}, index={self.i})"

    def change_frequency(self, frequency):
        self.frequency = frequency

    def change_note_length(self, note_length):
        self.note_length = note_length

    def calc_duration_seconds(self, tempo, ticks_per_beat):
        self.duration_seconds = (float(self.note_length) / ticks_per_beat) * (tempo / 1000000.0)
        return self.duration_seconds
    
    def link_note(self, note):
        self.linked_notes.append(note)
    
    # Separating nearby notes from concurrent notes
    def relate_note(self, note):
        self.linked_notes.remove(note)
        self.nearby_notes.append(note)

    def note_ends_timestamp(self):
        return self.timestamp + self.note_length
    
    def separate_notes_by_concurrency(self):
        notes_to_move = list()
        for note in self.linked_notes:
            if note.note_ends_timestamp() < self.timestamp:
                notes_to_move.append(note)
            elif self.timestamp > note.note_ends_timestamp():
                notes_to_move.append(note)

        for note in notes_to_move:
            self.relate_note(note)
    
    def set_index(self, index):
        self.i = index

    def unique_linked_notes(self):
        note_nums = list()
        unique_nums = list()

        for note in self.linked_notes:
            note_nums.append(note.note)

        for num in note_nums:
            num = num % 12
            if num not in unique_nums:
                unique_nums.append(num)
        
        return unique_nums
    
    def unique_nearby_notes(self):
        note_nums = list()
        unique_nums = list()

        for note in self.nearby_notes:
            note_nums.append(note.note)

        for num in note_nums:
            num = num % 12
            if num not in unique_nums:
                unique_nums.append(num)
        
        return unique_nums
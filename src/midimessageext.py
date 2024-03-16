class MidiMessageExt:
    def __init__(self, channel, note, velocity, timestamp):
        self.channel = channel
        self.note = note
        self.velocity = velocity
        self.timestamp = timestamp
        self.i = -1
        self.note_length = -1 
        self.bass_tuning = -1
        self.is_major = 1
        self.duration_seconds = -1.0 
        self.linked_notes = list()
        self.nearby_notes = list()

    def __repr__(self):
        return f"\nMidiMessageExt(channel={self.channel}, note={self.note}, velocity={self.velocity}, timestamp={self.timestamp}, note_length={self.note_length}, tuning={self.bass_tuning}-{self.is_major}, duration_seconds={self.duration_seconds}, index={self.i})"

    def __str__(self):
        return f"\nMidiMessageExt(channel={self.channel}, note={self.note}, velocity={self.velocity}, timestamp={self.timestamp}, note_length={self.note_length}, tuning={self.bass_tuning}-{self.is_major}, duration_in_seconds={self.duration_seconds}, index={self.i})"

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

        note_nums.append(self.note)

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
    
    def set_tuning(self):
        is_consistent = 1
        curr_tuning = -1
        is_major = -1

        for note in self.linked_notes:
            if note.bass_tuning != -1:
                if curr_tuning == -1:
                    if self.is_in_chord(self.note, note.bass_tuning, note.is_major):
                        curr_tuning = note.bass_tuning
                        is_major = note.is_major
                    else:
                        is_consistent = 0
                        break
                elif curr_tuning == note.bass_tuning:
                    continue # Notes are consistent
                elif curr_tuning != note.bass_tuning:
                    is_consistent = 0
                    break # No reason to continue, can't rely on previous tuning

        if is_consistent and curr_tuning != -1:
            # We have decided that all previous notes agree on 
            # tuning and that the current note matches the tuning, 
            # so set tuning to match other notes
            self.bass_tuning = curr_tuning 
            self.is_major = is_major
            return
        elif curr_tuning != -1:
            # We have multiple simultaneous chords due to being unsure of tuning
            # For now, set current note to be its own root
            self.bass_tuning = self.note % 12
            self.is_major = 1
            return
        else:
            # First note in new chord, need completely new handling
            linked_note_nums = self.unique_linked_notes()
            for root in linked_note_nums:
                is_chord, is_major = self.check_all_notes_in_chord(root, linked_note_nums)
                if is_chord:
                    self.bass_tuning = root
                    self.is_major = is_major
                    return

            if not is_chord:
                #TODO need to write more advanced analysis here
                return


    # Takes MidiMessageExt.note for two notes and MidiMessageExt.is_major for
    # root note and checks if note is in a chord based on root
    # note: int - note num for note to check
    # root: int - note num for root note
    # is_major: boolean - value for if root chord is major or minor
    def is_in_chord(self, note, root, is_major):
        dist = self.note_dist(root, note)

        if dist == 0:
            return True
        elif (dist == 4 or dist == 7 or dist == 10) and is_major:
            return True
        elif (dist == 3 or dist == 7 or dist == 10) and not is_major:
            return True
        else:
            return False

    # Takes MidiMessageExt.note for two notes, returns distance
    # root: int - note num of root note
    # note: int - note num of note to check
    def note_dist(self, root, note):
        dist = (note % 12) - (root % 12)

        if dist >= 0:
            return dist
        else:
            return ((note % 12) + 12) - (root % 12)
        
    # Takes MidiMessageExt.note for root and list, checks if there 
    # is a chord that can be formed from root and list of notes
    # Returns two booleans for is_major and is_chord
    # root: int - note num of root note
    # list: list(int) - list of note nums to check against root
    def check_all_notes_in_chord(self, root, list):
        sum = 0
        # Check if chord is major
        for note in list:
            sum += self.is_in_chord(note, root, 1)

        if sum == len(list):
            return True, True
        else:
            # Check if chord is minor
            sum = 0
            for note in list:
                sum += self.is_in_chord(note, root, 0)
            
            if sum == len(list):
                return True, False
            else:
                return False, False

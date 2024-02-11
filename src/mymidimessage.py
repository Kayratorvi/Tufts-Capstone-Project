class MidiMessageExt:
    def __init__(self, channel, note, velocity, delta_time, timestamp):
        self.channel = channel
        self.note = note
        self.velocity = velocity
        self.delta_time = delta_time
        self.timestamp = timestamp
        self.note_length = -1
        self.frequency = 0.0

    def __repr__(self):
        return f"MidiMessageExt(channel={self.channel}, note={self.note}, velocity={self.velocity}, time={self.delta_time}, timestamp={self.timestamp}, note_length={self.note_length}, tuning={self.frequency})\n"

    def __str__(self):
        return f"MidiMessageExt(channel={self.channel}, note={self.note}, velocity={self.velocity}, time={self.delta_time}, timestamp={self.timestamp}, note_length={self.note_length}, tuning={self.frequency})\n"

    def change_frequency(self, frequency):
        self.frequency = frequency

    def change_note_length(self, note_length):
        self.note_length = note_length
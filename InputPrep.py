from mido import MidiFile
import mido
import sys
import numpy as np
from pypianoroll import Multitrack, Track
from matplotlib import pyplot as plt

class MidiParser:

    def parse_file(self, filename, track_type):
        return self.midi2piano_roll2(filename, track_type)

    def midi2piano_roll2(self, filename, track_type):

        program_range = None
        if track_type=='piano':
            program_range = (0, 8)
        elif track_type=='guitar':
            program_range = (25, 32)
        elif track_type=='bass':
            program_range = (33, 40)

        midi = Multitrack(filename)
        for track in midi.tracks:
            if program_range[0] <= track.program <= program_range[1]:
                return track.pianoroll

        print('couldn\'t find {} track in midi file {}'.format(track_type, filename))


        #fig, ax = mul.plot()
        #plt.show()

    def get_training_data(self, piano_roll):
        None

if __name__=="__main__":
    parser = MidiParser()
    piano_roll = parser.parse_file('2MinutesToMidnight.mid', 'guitar')
    print(type(piano_roll))
    print(piano_roll.shape)




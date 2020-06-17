import sys
import os
import numpy as np
from pypianoroll import Multitrack, Track
from matplotlib import pyplot as plt

class MidiParser:

    def parse_files(self, directory, track_type):
        data_x = []
        data_y = []

        for file in os.listdir(directory):

            print(directory + '/' + file)
            piano_roll = self.parse_file(directory + '/' + file, track_type)
            temp_x, temp_y = self.get_training_data_multi(piano_roll)
            print('temp_x shape:', temp_x.shape)
            print('temp_y shape:', temp_y.shape)
            if len(data_x) == 0 and len(data_y) == 0:
                data_x = temp_x
                data_y = temp_y
            else:
                data_x = np.concatenate([data_x, temp_x], axis=0)
                data_y = np.concatenate([data_y, temp_y], axis=0)
            print('data_x shape:', data_x.shape)
            print('data_y shape:', data_y.shape)
        return data_x, data_y

    def parse_file(self, filename, track_type):
        return self.midi2piano_roll(filename, track_type)

    def midi2piano_roll(self, filename, track_type):

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


    def get_training_data_single(self, piano_roll):
        example_length = 50
        label_length = 1
        examples = []
        labels = []

        i = 0
        while i + example_length + label_length < len(piano_roll):
            examples.append(piano_roll[i:i + example_length, :])
            labels.append(piano_roll[i + example_length:i + example_length + label_length, :])
            i += example_length + label_length
        return np.array(examples), np.array(labels)

    def get_training_data_multi(self, piano_roll):
        example_length = 10
        examples = []
        labels = []

        i = 0
        while i + example_length + 1 < len(piano_roll):
            examples.append(piano_roll[i:i + example_length, :])
            labels.append(piano_roll[i + 1:i + 1 + example_length, :])
            i += example_length + 1
        return np.array(examples), np.array(labels)

if __name__=="__main__":
    parser = MidiParser()
    #piano_roll = parser.parse_file('2MinutesToMidnight.mid', 'piano')
    #print(type(piano_roll))
    #print(piano_roll.shape)
    np.set_printoptions(threshold=sys.maxsize)

   # data_x, data_y = parser.get_training_data_multi(piano_roll)
    data_x, data_y = parser.parse_files('test_files', 'guitar')
    # with open('x.txt', 'w') as f:
    #     f.write(np.array2string(train_x[0].T[:, :]))
    # with open('y.txt', 'w') as f:
    #     f.write(np.array2string(train_y[0].T[:, :]))
    print('training data shape:', data_x.shape)
    print('training label shape:', data_y.shape)


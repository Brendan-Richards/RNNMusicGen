import sys
import os
import numpy as np
from pypianoroll import Multitrack, Track
from matplotlib import pyplot as plt
import pickle

class MidiParser:

    def parse_files(self, directory, track_type):
        data_x = []
        data_y = []
        total = 0
        bytes = 0
        for file in os.listdir(directory):

            print(directory + '/' + file)
            try:
                piano_roll = self.parse_file(directory + '/' + file, track_type)
            except:
                print('couldn\'t parse file for some reason. skipping')
                continue
            if piano_roll is None:
                continue
            temp_x, temp_y = self.get_training_data_multi(piano_roll)
            total += len(temp_x)
            bytes += temp_x.nbytes
            # print('temp_x shape:', temp_x.shape)
            # print('temp_y shape:', temp_y.shape)
            if len(data_x) == 0 and len(data_y) == 0:
                data_x.append(temp_x)
                data_y.append(temp_y)
            else:
                data_x.append(temp_x)
                data_y.append(temp_y)
                # data_x = np.concatenate([data_x, temp_x], axis=0)
                # data_y = np.concatenate([data_y, temp_y], axis=0)
            print('num examples:', total)
            print('size:', (bytes/1073741824), 'Gigabytes')
            #print('data shape:', data_x.shape)
        print('concatenating: ')
        return np.concatenate(data_x, axis=0), np.concatenate(data_y, axis=0)

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
        return None


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
        example_length = 100
        examples = []
        labels = []

        i = 0
        while i + example_length + 1 < len(piano_roll):
            examples.append(piano_roll[i:i + example_length, :])
            labels.append(piano_roll[i + 1:i + 1 + example_length, :])
            i += example_length + 1
        return np.array(examples), np.array(labels)

def make_rock_guitar_data():
    parser = MidiParser()
    data_x, data_y = parser.parse_files('midi_training_files/rock', 'guitar')

    with open('data_x.pkl', 'wb') as file:
        pickle.dump(data_x, file, protocol=4)
    with open('data_y.pkl', 'wb') as file:
        pickle.dump(data_y, file, protocol=4)

    print('training data shape:', data_x.shape)
    print('training label shape:', data_y.shape)

def load_rock_guitar_data():
    with open('pickles/data_rock_guitar_x.pkl', 'rb') as file:
        data_x = pickle.load(file)
    with open('pickles/data_rock_guitar_y.pkl', 'rb') as file:
        data_y = pickle.load(file)

    return data_x, data_y

if __name__=="__main__":
    make_rock_guitar_data()






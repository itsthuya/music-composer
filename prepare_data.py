import os
import pickle

from music21 import converter, instrument, note, chord
from multiprocessing import Pool, cpu_count


def extract_notes(file):
    notes = []
    midi = converter.parse(file)
    parts = instrument.partitionByInstrument(midi)

    if parts:  # file has instrument parts
        notes_to_parse = parts.parts[0].recurse()
    else:  # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))

    print("Completed {}".format(file))
    return notes


if __name__ == '__main__':
    folder = 'data'
    file_list = os.listdir(folder)
    file_list = [os.path.join(folder, x) for x in file_list]

    with Pool(processes=1) as pool:
        results = pool.map(extract_notes, file_list)

    notes = []
    for result in results:
        notes = notes + result

    print(notes)
    with open('notes.pkl', 'wb') as f:
        pickle.dump(notes, f, protocol=pickle.HIGHEST_PROTOCOL)

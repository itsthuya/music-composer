import os
import pickle

from music21 import converter, instrument, note, chord
from multiprocessing import Pool, cpu_count


def extract_notes(file):
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


if __name__ == '__main__':
    file_list = os.listdir('data')

    notes = []
    with Pool(processes=cpu_count()-1) as pool:
        pool.map(extract_notes, file_list)

    with open(os.path.join('data', 'notes.pickle'), 'wb') as f:
        pickle.dump(notes, f, protocol=pickle.HIGHEST_PROTOCOL)

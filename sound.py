
import re
import pandas as pd

def chord_to_notes(chord):

    """
    Finds the notes belonging to a chord. 
    Starts the chord in the 4th octave and adds a bass note in the 3rd octave. 

    Args:
        chord: str
  
    Returns:
        notes: tuple of strings. 
    """

    # https://www.songtive.com/chords/piano
    additions = {"m" : (3, 7), 
                "dim" : (3, 6), 
                "maj7" : (4, 7, 11), 
                "m7" : (3, 7, 10), 
                "sus2" : (2, 7), 
                "sus4" : (5, 7), 
                "aug" : (4, 8), 
                "maj11" : (4, 7, 11, 14, 17),
                "maj6" : (4, 7, 9), 
                "m6" : (3, 7, 9),
                "add2" : (2, 4, 7),
                "add4" : (4, 5, 7), 
                "add9" : (4, 7, 14), 
                "7" : (4, 7, 10), 
                "7sus4" : (5, 7, 10), 
                "dim7" : (3, 6, 9), 
                "9" : (4, 7, 10, 14), 
                "m9" : (3, 7, 10, 14), 
                "maj9" : (4, 7, 11, 14), 
                "11" : (4, 7, 10, 14, 17), 
                "madd4" : (3, 5, 7),
                "5" : (5),
                "6" : (4, 7, 9),
                "2" : (3, 4, 7)}

    # Find the note intervals for the chord. 

    pattern = re.compile(r"[A-G][#]*([a-z0-9]*)[\/]*[A-G]*[#]*")
    result = pattern.search(chord)

    if result.group(1) == "":
        chordtuple = (4, 7)
    else:

        addition = pattern.search(chord).group(1)

        try:
            chordtuple = additions[addition]
        except KeyError:
            raise KeyError("The chord is not defined.")

    # Find the root and bass note. 

    pattern = re.compile(r"[A-G][#]*")
    matches = pattern.findall(chord)

    root = matches[0]
    if len(matches) == 1:
        bass = matches[0]
    else:
        bass = matches[1]

    # Find the actual notes in the chord.

    notes = ["C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
            "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
            "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5"]

    rootindex = notes.index(root + "4")
    chordnotes = [bass + "3", root + "4"]

    for interval in chordtuple:
        chordnotes.append(notes[rootindex + interval])

    return chordnotes

def note_to_pitch(note):

    pitches = pd.read_csv("frequencies.csv")
    pitch = float(pitches['Frequency'][pitches['Note'] == note])

    return pitch
    
def write_midi(chord_sequence):

    # Change chords to notes (list of tuples?) -> def chord_to_notes(chord)
    # Change notes to pitches (list of tuples?) -> def note_to_pitch(note), https://pages.mtu.edu/~suits/notefreqs.html
    # Write pitches to midi file:
    #   https://midiutil.readthedocs.io/en/latest/
    #   https://stackoverflow.com/questions/11059801/how-can-i-write-a-midi-file-with-python

    return midifile

if __name__ == "__main__":

    print(note_to_pitch("G#5"))
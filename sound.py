
def chord_to_notes(chord):

    """
    Finds the notes belonging to a chord. 
    Starts the chord in the 4th octave and adds a bass note in the 3rd octave. 

    Args:
        chord: str
  
    Returns:
        notes: tuple of strings. 
    """

    notes = ["C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
            "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
            "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5"]

    # Only check before a / sign. Look for an addition after the starting capital letter (and possibly a '#')
    # Flats should already be removed at this point. 

    # Also implement an error for when the chord is not found! 

    return(chordnotes)

def write_midi(chord_sequence):

    # Change chords to notes (list of tuples?) -> def chord_to_notes(chord)
    # Change notes to pitches (list of tuples?) -> def note_to_pitch(note), https://pages.mtu.edu/~suits/notefreqs.html
    # Write pitches to midi file, https://midiutil.readthedocs.io/en/latest/

    


    return midifile
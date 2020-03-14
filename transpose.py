
import re

def transposeNote (note, distance):

    """
    Parameters
    ----------
    note : str
        One of the following: "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
    distance : int
        Distance to transpose with. 
    """

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    if note not in notes :
        raise ValueError("The note is undefined.")

    transindex = notes.index(note) + distance

    if transindex > 11:
        transindex = transindex - 12
    elif transindex < 0:
        transindex = transindex + 12

    transnote = notes[transindex]

    return (transnote)

def transposeChord (chord, distance):

    """
    Parameters
    ----------
    chord : str
        A chord that starts with a capital letter. Base note behind forward slash is supported.
    distance : int
        Distance to transpose with. 
    """

    pattern = re.compile(r"[A-G][#]*")
    matches = pattern.findall(chord)

    for match in matches:
        transmatch = transposeNote(match, distance)
        chord = re.sub(match, transmatch, chord)

    return (chord)

def equiChord (chord):

    """
    Parameters
    ----------
    chord : str
        A flat chord that starts with a capital letter.
    """

    equiChords = {"Db":"C#", "Eb":"D#", "Gb":"F#", "Ab":"G#", "Bb":"A#"}

    if chord not in equiChords.keys() :
        raise ValueError("The chord doesn't need an equivalent version.")

    pattern = re.compile(r"[A-G]+[b]+")
    matches = pattern.findall(chord)

    for match in matches:
        equiChord = equiChords.get(match)

    return (equiChord)



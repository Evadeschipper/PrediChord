
# Training can be done with all of the data because prediction will basically be done based on our input?
# So define train function
# Make predict function based on probabilities derived from training the data
# sklearn or nlptk for training ngrams?

import pickle
from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
from numpy.random import choice

def train_trigrams(data):

    """
    Build trigram model from chord data. 

    Args:
        data: dict - keys are links, values are lists of chords.
  
    Returns:
        model: dictionary of dictionaries containing probabilities of chord following two other chords.
    """

    # Create a placeholder for model
    model = defaultdict(lambda: defaultdict(lambda: 0))

    # Count frequency of co-occurance  
    for chords in data.values():
        for w1, w2, w3 in trigrams(chords, pad_right=True, pad_left=True):
            model[(w1, w2)][w3] += 1
    
    # Let's transform the counts to probabilities
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            model[w1_w2][w3] /= total_count

    return model

def train_bigrams(data):

    """
    Build bigram model from chord data. 

    Args:
        data: dict - keys are links, values are lists of chords.
  
    Returns:
        model: dictionary of dictionaries containing probabilities of a chord following a chord.
    """

    # Create a placeholder for model
    model = defaultdict(lambda: defaultdict(lambda: 0))

    # Count frequency of co-occurance  
    for chords in data.values():
        for w1, w2 in bigrams(chords, pad_right=True, pad_left=True):
            model[w1][w2] += 1
    
    # Let's transform the counts to probabilities
    for w1 in model:
        total_count = float(sum(model[w1].values()))
        for w2 in model[w1]:
            model[w1][w2] /= total_count

    return model

def generate_chord(pre, model):
    
    """
    Generates a chord based on chord(s) input, stochastically, based on model probabilities. 

    Args:
        pre: either a string (for one chord) or a tuple of strings (for several chords). 
        model: dictionary of dictionaries containing probabilities of a chord following (a) chord(s).
  
    Returns:
        chord: str - generated chord. 
    """

    pre_dict = model.get(pre)

    post_chords = []
    post_probs = []

    for postchord in pre_dict:

        post_chords.append(postchord)
        post_probs.append(pre_dict.get(postchord))
    
    chord = choice(a = post_chords, size = 1, p = post_probs)
    while None in chord:
        chord = choice(a = post_chords, size = 1, p = post_probs)

    chord = ''.join(chord)

    return chord

def generate_sequence(inputchord, model, n):

    """
    Generates a chord sequence based on chord(s) input. 

    Args:
        input: either a string (for one chord) or a tuple of strings (for several chords). 
        model: dictionary of dictionaries containing probabilities of a chord following (a) chord(s).
        n: int - length of sequence to generate.
  
    Returns:
        sequence: list - list with generated chords (str).  
    """

    sequence = [inputchord]
    
    i = 0
    while i < n:
        
        inputchord = generate_chord(inputchord, model)
        sequence.append(inputchord)
        i += 1

    return sequence

if __name__ == "__main__":

    with open('tempdata.pickle', 'rb') as handle:
        data = pickle.load(handle)

    model = train_bigrams(data)

    inputchord = "Em"
    sequence = generate_sequence(inputchord, model, 20)
    print(sequence)

        
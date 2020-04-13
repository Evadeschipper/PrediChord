
# Training can be done with all of the data because prediction will basically be done based on our input?
# So define train function
# Make predict function based on probabilities derived from training the data
# sklearn or nlptk for training ngrams?

import pickle
from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
from numpy.random import choice
from abc import ABC, abstractmethod


class ChordModel(ABC):
    @abstractmethod
    def fit(self, data):
        pass


    @abstractmethod
    def generate_chord(self, start_sequence=None):
        pass


    @abstractmethod
    def generate_sequence(self, n, start_sequence=None):
        pass


class Ngram(ChordModel):
    def __init__(self, N=3):
        if N not in [2, 3]:
            raise NotImplementedError("Only bigrams and trigrams supported (N=2, N=3)")

        self.model = defaultdict(lambda: defaultdict(lambda: 0))
        self.n = N


    def fit(self, data):
        """
        Train the model on the chord data. Model (dictionary of dictionaries containing probabilities of chord following other chord(s))
        accessible through class attribute 'model'.

        Args:
            data: dict - keys are links, values are lists of chords.
    
        Returns:
            None
        """
        # Count frequency of co-occurance
        if self.n == 3:
            for chords in data.values():
                for w1, w2, w3 in trigrams(chords, pad_right=True, pad_left=True):
                    self.model[(w1, w2)][w3] += 1
        elif self.n == 2:
            for chords in data.values():
                for w1, w2 in bigrams(chords, pad_right=True, pad_left=True):
                    self.model[(w1,)][w2] += 1
        else:
            raise NotImplementedError("Only bigrams and trigrams supported (N=2, N=3)")

        
        # Let's transform the counts to probabilities
        for pre_chords in self.model:
            total_count = float(sum(self.model[pre_chords].values()))
            for w3 in self.model[pre_chords]:
                self.model[pre_chords][w3] /= total_count


    def generate_chord(self, start_sequence=None):
        """
        Generates a chord based on chord(s) input, stochastically, based on model probabilities. 

        Args:
            start_sequence: either a string (for one chord) or a tuple of strings (for several chords).
    
        Returns:
            chord: str - generated chord. 
        """

        if start_sequence is None:
            # Take a random key as a starting point
            start_idx = choice(len(self.model.keys()), size=1)[0]
            start_sequence = list(self.model.keys())[start_idx]
        

        pre_dict = self.model.get(start_sequence)

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


    def generate_sequence(self, n, start_sequence=None):

        """
        Generates a chord sequence based on chord(s) input. 

        Args:
            n: int - length of sequence to generate.
            start_sequence: either a string (for one chord) or a tuple of strings (for several chords). 
    
        Returns:
            sequence: list - list with generated chords (str).  
        """

        if start_sequence is None:
            # Take a random key as a starting point
            start_idx = choice(len(self.model.keys()), size=1)[0]
            start_sequence = list(self.model.keys())[start_idx]

        sequence = [*start_sequence]
        
        i = 0
        while i < n:
            
            inputchord = self.generate_chord(start_sequence=tuple(sequence[-(self.n-1):]))
            sequence.append(inputchord)
            i += 1

        return sequence

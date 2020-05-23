import json
import csv
import pickle
import pandas as pd
from os import listdir
from predict import train_bigrams, train_trigrams, generate_sequence
from sound import write_midi

jsonfiles = listdir("data/cache")
data = {}

for jsonfile in jsonfiles:

    with open("data/cache/{}".format(jsonfile), encoding="utf8") as f:

        chords = json.load(f)["Chords"]
        if len(chords) is not 0:
            data[jsonfile] = chords

with open('data/chords.pickle', 'wb') as handle:
    pickle.dump(data, handle)

if __name__ == "__main__":

    with open('data/chords.pickle', 'rb') as handle:
        data = pickle.load(handle)

    model = train_bigrams(data)

    inputchord = "Em"
    i = 0

    while i <= 10: 

        sequence = generate_sequence(inputchord, model, 10)
        filepath = "results/" + '-'.join(sequence).replace("/", "_")
        write_midi(sequence, filepath)

        i += 1

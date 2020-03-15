
# Training can be done with all of the data because prediction will basically be done based on our input?
# So define train function
# Make predict function based on probabilities derived from training the data
# sklearn or nlptk for training ngrams?

import pickle
from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict

if __name__ == "__main__":

    with open('tempdata.pickle', 'rb') as handle:
        data = pickle.load(handle)
    
    print(trigrams(data["https://tabs.ultimate-guitar.com/tab/adele/when-we-were-young-chords-1782038"]))

"""     # Create a placeholder for model
    model = defaultdict(lambda: defaultdict(lambda: 0))

    # Count frequency of co-occurance  
    for songchords in data.items():
        for w1, w2, w3 in trigrams(songchords, pad_right=True, pad_left=True):
            model[(w1, w2)][w3] += 1
    
    # Let's transform the counts to probabilities
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w3 in model[w1_w2]:
            model[w1_w2][w3] /= total_count
    
    for key, value in model:
        print(key, value) """

        
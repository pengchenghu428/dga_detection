import pickle
from collections import defaultdict

def bigrams(words):
    wprev = None
    for w in words:
        if not wprev==None:
            yield (wprev, w)
        wprev = w
        
def hmm_prob(domain):
    bigram = [''.join((i,j)) for i,j in bigrams(domain) if not i==None]
    prob = transitions[''][bigram[0]]
    for x in range(len(bigram)-1):
        next_step = transitions[bigram[x]][bigram[x+1]]
        prob *= next_step

    return prob

def train(data, trans_matrix_path, n_grams=2):
    words = [w.strip().lower() for w in data]
    words = ["^" + w.split('/')[0] + "$" for w in words if w != ""]
    transitions = defaultdict(lambda: defaultdict(float))
    n = n_grams
    for word in words:
        if len(word) >= n:
            transitions[""][word[:n]] += 1.0
        for i in range(len(word) - n):
            gram = word[i : i + n]
            next_ = word[i + 1 : i + n + 1]
            transitions[gram][next_] += 1.0
    
    # normalize the probabilities
    for gram in transitions:
        total = sum([transitions[gram][next_] for next_ in transitions[gram]])
        for next_ in transitions[gram]:
            transitions[gram][next_] /= total
            
    with open(trans_matrix_path, mode='w') as fw:
        for key1, dict1 in transitions.items():
            for key2, value in dict1.items():
                fw.write('%s\t%s\t%f\n'%(key1,key2,value))
                
def load_trans_matrix(trans_matrix_path):
    transitions = defaultdict(lambda: defaultdict(float))  # 加载
    with open(trans_matrix_path, mode='r') as f_trans:
        for f in f_trans:
            key1,key2,value =f.rstrip().split('\t')
            value = float(value)
            transitions[key1][key2] = value
    return transitions

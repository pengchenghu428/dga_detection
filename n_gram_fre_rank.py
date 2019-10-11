import tldextract
import numpy as np
from collections import defaultdict

def ave(array_):#sanity check for NaN
    if len(array_)>0:
        return array_.mean()
    else:
        return 0
    
def std(array_):#sanity check for NaN
    if len(array_)>0:
        return array_.std()
    else:
        return 0
 
def bigrams(words):   # 2grams
    wprev = None
    for w in words:
        if not wprev==None:
            yield (wprev, w)
        wprev = w
 
def trigrams(words):  # 3grams
    wprev1 = None
    wprev2 = None
    for w in words:
        if not (wprev1==None or wprev2==None):
            yield (wprev1,wprev2, w)
        wprev1 = wprev2
        wprev2 = w
        
def generate_n_gram_freq_file(data, output_path):
    unigram_rank = defaultdict(int)
    bigram_rank = defaultdict(int)
    trigram_rank = defaultdict(int)
    
    for f in data:
        # rank,domain = f.strip().split(',')
        domain = f
        ext = tldextract.extract(domain)
        tld = ext.suffix
        main_domain = '$'+ext.domain+'$'#add begin and end
        for i in main_domain[1:-1]:
            unigram_rank[i]+=1
        for i in bigrams(main_domain):
            bigram_rank[''.join(i)]+=1
        for i in trigrams(main_domain):
            trigram_rank[''.join(i)]+=1
    
    with open(output_path, 'w') as fw:
        for rank,(i,freq)in enumerate(sorted(unigram_rank.items(), key = lambda x:x[1], reverse = True)):
            try:
                fw.write('1,%s,%d,%d\n'%(i,freq,rank+1))
            except UnicodeEncodeError:
                continue
        for rank,(i,freq) in enumerate(sorted(bigram_rank.items(),key = lambda x:x[1], reverse = True)):
            try:
                fw.write('2,%s,%d,%d\n'%(i,freq,rank+1))
            except UnicodeEncodeError:
                continue
        for rank,(i,freq) in enumerate(sorted(trigram_rank.items(),key = lambda x:x[1], reverse = True)):
            try:
                fw.write('3,%s,%d,%d\n'%(i,freq,rank+1))
            except UnicodeEncodeError:
                continue
 
def load_n_gram_fre_rank(n_gram_freq_path):
    # 获取数据
    gram_rank_dict = dict()
    with open(n_gram_freq_path, 'r') as n_gram_file:
        for i in n_gram_file:
            cat,gram,freq,rank = i.strip().split(',')
            gram_rank_dict[gram]=int(rank)
    return gram_rank_dict
    
    
def count_n_gram(domain, gram_rank_dict):
    main_domain = '$' + domain +'$'
    bigram = [''.join(i) for i in bigrams(main_domain)]  # extract the bigram
    trigram = [''.join(i) for i in trigrams(main_domain)]  # extract the bigram
    unigram_rank = np.array([gram_rank_dict[i] if i in gram_rank_dict else 0 for i in main_domain[1:-1]])
    bigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in bigrams(main_domain)])
    trigram_rank = np.array([gram_rank_dict[''.join(i)] if ''.join(i) in gram_rank_dict else 0 for i in trigrams(main_domain)])
    return np.array([ave(unigram_rank),ave(bigram_rank),ave(trigram_rank),
                      std(unigram_rank),std(bigram_rank),std(trigram_rank)])
 
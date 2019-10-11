import numpy as np
from collections import Counter
from itertools import groupby

def count_entropy(domain):
    domain_len = len(domain)
    count = Counter(i for i in domain).most_common()
    entropy = -sum(fre / domain_len * (np.log(fre/domain_len)) for ch, fre in count)
    return entropy
    
def count_vowel_ratio(domain):
    vowels=list('aeiou')
    sum_vowel = sum(vowels.count(i) for i in domain.lower())
    return sum_vowel / len(domain) if sum_vowel > 0 else 0


def count_digits_ratio(word):#how many digits
    digits=list('0123456789')
    sum_digits = sum(digits.count(i) for i in word.lower())
    return sum_digits / len(word) if sum_digits > 0 else 0
    

def count_repeat_letter(word):
    count = Counter(i for i in word.lower() if i.isalpha()).most_common()
    cnt = 0
    for letter,ct in count:
        if ct>1:
            cnt+=1
    return cnt / len(word) if cnt > 0 else 0
    
def consecutive_digits_ratio(word):#how many consecutive digit
    cnt = 0
    digit_map = [int(i.isdigit()) for i in word]
    consecutive=[(k,len(list(g))) for k, g in groupby(digit_map)]
    count_consecutive = sum(j for i,j in consecutive if j>1 and i==1)
    return count_consecutive / len(word) if count_consecutive > 0 else 0
    
def consecutive_consonant(word):#how many consecutive consonant
    cnt = 0
    consonant = set(['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 
                     'n', 'p', 'q', 'r', 's', 't', 'v', 'w','x', 'y', 'z'])
    digit_map = [int(i in consonant) for i in word]
    consecutive=[(k,len(list(g))) for k, g in groupby(digit_map)]
    count_consecutive = sum(j for i,j in consecutive if j>1 and i==1)
    return count_consecutive / len(word) if count_consecutive > 0 else 0
    


from curses.ascii import isalnum, isalpha, isspace
import nltk
from nltk.tokenize import word_tokenize
import os
from collections import Counter

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download("stopwords")

def Tokenize(s):
    s = ''.join(filter(lambda c: isalnum(c) or isspace(c), s.lower()))
    words = word_tokenize(s) 
    lemmatizer = nltk.stem.WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

def SaveCounts(counts, output_file):
    with open(output_file, 'w') as f:
        for word, count in counts.most_common():
            f.write(f'{word}\t{count}\n')

def GetCountsFromFileBig(input_file):
    counts = {}
    with open(input_file, "r") as f:
        i=0
        for l in f:
            i+=1
            tokens = Tokenize(l)
            for t in tokens:
                if t not in counts:
                    counts[t] = 1
                else: 
                    counts[t] += 1
            if ( i % 100000 == 0 ):
                print(i)

def GetCounts(s):
    return Counter(Tokenize(s))

def GetCountsFromFile(input_file):
    return GetCounts(open(input_file, "r").read())

def ProcessData():
    i = 0
    for f in os.listdir('data/parsed'):
        if f.endswith('.txt'):
            i+=1
            target = os.path.join('data/tokenized', f)
            counts = GetCountsFromFile(os.path.join('data/parsed', f))
            SaveCounts(counts, target)
            print(i, "files processed", end='\r')




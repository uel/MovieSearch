import matplotlib.pyplot as plt

def dist():
    y = []
    x = []
    with open('data/merged_tokens.txt', 'r') as f:
        for i in range(1000):
            line = f.readline().strip().split('\t')
            y.append(int(line[1]))
            x.append(line[0])
        

    x = x[::50]
    y = y[::50]

    plt.plot(x, y)
    plt.show()

def loglogdist():
    import math
    stopwords = 0
    words = 0
    lex_size = 0

    frequencies = []
    x = []
    for i, l in enumerate(open("data/merged_tokens.txt")):
        term, freq = l.split("\t")
        freq = int(freq)
        frequencies.append(math.log(freq))
        x.append(math.log(i+1))
        if freq <= 1 or freq > 750000:
            stopwords += freq
        else:
            lex_size += 1
            words += freq

    print("Stopwords:", stopwords)
    print("Words:", words)
    print("Lexicon size:", lex_size)

    plt.plot(x, frequencies)
    plt.show()
import os

max_freq = {}

for i in os.listdir("data/tokenized"):
    with open("data/tokenized/" + i, "r") as f:
        for l in f:
            term, freq = l.split("\t")
            freq = int(freq)
            if term in max_freq:
                if freq > max_freq[term]:
                    max_freq[term] = freq
            else:
                max_freq[term] = freq

with open("data/max_freq.txt", "w") as f:
    for i, j in max_freq.items():
        f.write(i + "\t" + str(j) + "\n")

df = {}

for i in os.listdir("data/tokenized"):
    with open("data/tokenized/" + i, "r") as f:
        for l in f:
            term, freq = l.split("\t")
            freq = int(freq)
            if term in df:
                df[term] += 1
            else:
                df[term] = 1

with open("data/document_freq.txt", "w") as f:
    for i, j in df.items():
        f.write(i + "\t" + str(j) + "\n")
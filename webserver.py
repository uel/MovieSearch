from flask import Flask, g, request, jsonify
import sqlite3
import pexpect
import word_processing
import math
from gensim.models.doc2vec import Doc2Vec

DATABASE = 'subtitles.db'

index = pexpect.spawn('./search')
column_len = len(open('data/documents.txt', 'r').read().splitlines())
document_freq = {j.split("\t")[0] : int(j.split("\t")[1]) for j in open('data/document_freq.txt', 'r').read().splitlines()}
max_freq = {j.split("\t")[0] : int(j.split("\t")[1]) for j in open('data/max_freq.txt', 'r').read().splitlines()}

def search(query):
    counts = word_processing.GetCounts(query)
    args = ""
    for term, freq in counts.items():
        if term in max_freq:
            weight = (int(freq)/max_freq[term])*math.log2(column_len/document_freq[term])
            args += f"{term} {weight} "
    if args == "":
        return []
    index.sendline(args)
    index.expect("\n", timeout=None); index.expect("\n")
    return list(map(int, str(index.before)[2:-3].strip().split(" ")))


i2documents = { i : int(j) for i, j in enumerate(open('data/documents.txt', 'r').read().splitlines()) }
doc2vec_model = Doc2Vec.load("models/doc2vec.model")

def doc2vecSearch(query):
    vec = doc2vec_model.infer_vector(word_processing.Tokenize(query, True))
    res = doc2vec_model.dv.most_similar([vec], topn=50)
    return [i2documents[i] for i, _ in res]

app = Flask(__name__)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    return open('index.html').read()

@app.route("/movies")
def Movies():
    query = request.args.get('query')
    doc2vec = request.args.get('doc2vec')
    if query == "" or query == None:
        return "[]"

    if doc2vec == "true":
        ids = doc2vecSearch(query)
    else:
        ids = search(query)
    
    if ids == []:
        return "[]"
    
    i_ids = {j:i for i, j in enumerate(ids)}
    movies = get_db().execute('SELECT * FROM OpenSubtitles WHERE IDSubtitle IN '+str(tuple(ids))).fetchall()
    movies = sorted(list(movies), key=lambda x: i_ids[x['IDSubtitle']])
    return jsonify(movies)

app.run()
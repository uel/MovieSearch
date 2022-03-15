# from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec
import word_processing

# model = Doc2Vec(corpus_file='docs.cor', vector_size=512, window=2, min_count=2, workers=4)
# model.save('data/doc2vec.model')

#Doporučení, dokumentace

model = Doc2Vec.load("doc2vec/doc2vec.model")

new_vector = model.infer_vector(word_processing.Tokenize("you shall not pass", True))
sims = model.docvecs.most_similar([new_vector])
res = model.docvecs.most_similar(positive=[new_vector])
pass
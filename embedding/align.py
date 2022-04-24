from gensim.models import word2vec
import numpy as np

male_model = word2vec.Word2Vec.load("original/male.model")
female_model = word2vec.Word2Vec.load("original/female.model")

# Intersect vocabularies
shared_words = list(set(male_model.wv.index_to_key) & set(female_model.wv.index_to_key))

word_to_shared_idx = {}
for i, word in enumerate(shared_words):
    word_to_shared_idx[word] = i

new_male_indices = [male_model.wv.key_to_index[w] for w in shared_words]
male_model.wv.vectors = np.array([male_model.wv.vectors[i] for i in new_male_indices])

new_female_indices = [female_model.wv.key_to_index[w] for w in shared_words]
female_model.wv.vectors = np.array([female_model.wv.vectors[i] for i in new_female_indices])

male_model.wv.index_to_key = shared_words
female_model.wv.index_to_key = shared_words

male_model.wv.key_to_index = word_to_shared_idx
female_model.wv.key_to_index = word_to_shared_idx

# Procrustes alignment
M = (female_model.wv.vectors).T.dot(male_model.wv.vectors) 
U, _, V = np.linalg.svd(M)
R = U.dot(V) 
female_model.wv.vectors = (female_model.wv.vectors).dot(R)    

male_model.save("aligned/male.model")
female_model.save("aligned/female.model")

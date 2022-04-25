from gensim.models import word2vec
import numpy as np

male_model = word2vec.Word2Vec.load("original/male.model")
female_model = word2vec.Word2Vec.load("original/female.model")

male_model.init_sims(replace=True)
female_model.init_sims(replace=True)

# Intersect vocabularies
shared_words = list(set(male_model.wv.index_to_key) & set(female_model.wv.index_to_key))

male_shared_indices = [male_model.wv.key_to_index[w] for w in shared_words]
male_vectors = np.array([male_model.wv.vectors[i] for i in male_shared_indices])

female_shared_indices = [female_model.wv.key_to_index[w] for w in shared_words]
female_vectors = np.array([female_model.wv.vectors[i] for i in female_shared_indices])

# Procrustes alignment
M = (female_vectors).T.dot(male_vectors) 
U, _, V = np.linalg.svd(M)
R = U.dot(V)
female_model.wv.vectors = (female_model.wv.vectors).dot(R)    

male_model.save("aligned/male.model")
female_model.save("aligned/female.model")

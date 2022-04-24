from gensim.models import word2vec
import numpy as np

male_model = word2vec.Word2Vec.load("aligned/male.model")
female_model = word2vec.Word2Vec.load("aligned/female.model")

sim_scores = []

for word in male_model.wv.key_to_index.keys():
    if word in female_model.wv.key_to_index.keys():
        v_m = male_model.wv[word]
        v_f = female_model.wv[word]
        cos_sim = np.dot(v_m, v_f)/(np.linalg.norm(v_m) * np.linalg.norm(v_f))
        sim_scores.append((cos_sim, word))

sim_scores.sort()
f = open("sim_scores.csv", "w")
for score, word in sim_scores:
    f.write(word)
    f.write(",")
    f.write(str(score))
    f.write("\n")
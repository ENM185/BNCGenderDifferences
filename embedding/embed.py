from gensim.models import word2vec
import numpy as np

male_sentences = word2vec.LineSentence("../male_sentences.txt")
male_model = word2vec.Word2Vec(male_sentences, window=8, vector_size = 400)

female_sentences = word2vec.LineSentence("../female_sentences.txt")
female_model = word2vec.Word2Vec(female_sentences, window=8, vector_size = 400)

male_model.save("original/male.model")
female_model.save("original/female.model")

from sklearn.feature_extraction.text import TfidfVectorizer
import gensim.downloader as api
import numpy as np
from gensim.models import KeyedVectors

tokenizer_model = None

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

common_words = {"the":"","in":"","that":"","can":"","of":"","this":"","can":"","be":"","into":"",
"is":"","a":"","to":"","of":"","and":""}

def do_text_sim(query, corpus):
    global tokenizer_model

    if tokenizer_model is None:
        tokenizer_model = api.load('word2vec-google-news-300')

    search_term = query.split()
    search_embed = [tokenizer_model[word.lower()] for word in search_term if word.lower() in tokenizer_model]
    test = [word for word in search_term if word.lower() in tokenizer_model]; print(test)
    avg_search_embed = np.mean(search_embed, axis=0)

    scores = []
    for k in range(len(corpus)):
        terms = corpus[k].split()
        word_embeddings = [tokenizer_model[word.lower()] for word in terms if word.lower() in tokenizer_model and word.lower() not in common_words]
        if len(word_embeddings) == 0:
            scores.append(0); continue
        avg_embed = np.mean(word_embeddings, axis=0)
        scores.append(cosine_similarity(avg_search_embed, avg_embed))
    
    return scores


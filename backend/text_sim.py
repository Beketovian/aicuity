from sklearn.feature_extraction.text import TfidfVectorizer
import gensim.downloader as api
import numpy as np
from gensim.models import KeyedVectors

tokenizer_model = None

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

common_words = {"the":"","in":"","that":"","can":"","of":"","this":"","can":"","be":"","into":"",
"is":"","a":"","to":"","of":"","and":"", "how":"", "do":""}

def do_text_sim(query, input_dict):
    global tokenizer_model

    if tokenizer_model is None:
        tokenizer_model = api.load('word2vec-google-news-300')

    corpus = []
    for elems in input_dict:
        full_text = [txt["text"] for txt in elems]
        full_text = " ".join(full_text)
        corpus.append(full_text)
    
    search_term = query.split()
    search_term = [word.lower() for word in search_term]
    search_embed = [tokenizer_model[word.lower()] for word in search_term if word.lower() in tokenizer_model]
    test = [word for word in search_term if word.lower() in tokenizer_model]; print(test)
    avg_search_embed = np.mean(search_embed, axis=0)

    scores = []
    relevant_times = {i:[] for i in range(len(input_dict))}
    
    for i in range(len(input_dict)):
        word_embeddings = []
        for j in range(len(input_dict[i])):
            terms = input_dict[i][j]["text"].split()
            #word_embeddings = [tokenizer_model[word.lower()] for word in terms if word.lower() in tokenizer_model and word.lower() not in common_words]
            for word in terms:
                if word.lower() in tokenizer_model and word.lower() not in common_words:
                    word_embeddings.append(tokenizer_model[word.lower()])
                if word.lower() in search_term and word.lower() not in common_words:
                    relevant_times[i].append(input_dict[i][j]["start"])
                
        if len(word_embeddings) == 0:
            scores.append(0); continue
        avg_embed = np.mean(word_embeddings, axis=0)
        scores.append(cosine_similarity(avg_search_embed, avg_embed))
    
    return softmax(scores).tolist(), relevant_times


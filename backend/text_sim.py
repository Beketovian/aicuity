from sklearn.feature_extraction.text import TfidfVectorizer
import gensim.downloader as api
import numpy as np
from gensim.models import KeyedVectors

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

common_words = {
    "the":"",
    "in":"",
    "that":"",
    "can":"",
    "of":"",
    "this":"",
    "can":"",
    "be":"",
    "into":"",
    "is":"",
    "a":"",
    "to":"",
    "of":"",
    "and":""
}

def do_text_sim(corpus):
    #tokenizer_model = api.load('word2vec-google-news-300')  # Google's Word2Vec model
    # Load the Google News Word2Vec model
    model_path = 'GoogleNews-vectors-negative300.bin'  # Update with your actual file path
    tokenizer_model = KeyedVectors.load_word2vec_format(model_path, binary=True)

    search_term = "how do i eat a banana"
    search_term = search_term.split()
    search_embed = [tokenizer_model[word.lower()] for word in search_term if word.lower() in tokenizer_model]
    avg_search_embed = np.mean(search_embed, axis=0)


    for k in range(len(corpus)):
        terms = corpus[k].split()
        word_embeddings = [tokenizer_model[word.lower()] for word in terms if word.lower() in tokenizer_model and word.lower() not in common_words]
        # for term in terms:
        #     print(term)
        #print(len(word_embeddings))
        if len(word_embeddings) == 0:
            continue  # Return a zero vector if no words in the sentence are in the model
        avg_embed = np.mean(word_embeddings, axis=0)
        print(cosine_similarity(avg_search_embed, avg_embed))

in_string2 = """
IBM, or International Business Machines, traces its roots back to 1911, when it was originally founded as the Computing-Tabulating-Recording Company (CTR). A visionary leader, Thomas J. Watson, Sr., took the helm in 1914, and under his leadership, CTR evolved into IBM in 1924. Over the decades, IBM pioneered mainframes, ushered in the era of personal computers with its groundbreaking IBM PC in 1981, and later shifted focus to software and services, particularly artificial intelligence and cloud computing. With over a century of innovations, IBM remains a cornerstone in the tech industry.
"""

in_string3 = """
Eating a banana is a delightful and straightforward process that can be enjoyed in various ways. To start, select a ripe banana, which should have a bright yellow peel with a few brown spots indicating optimal sweetness. Hold the banana in one hand and gently peel it from the stem downwards, removing the skin completely. You can eat the banana directly by taking bites from the fruit, savoring its creamy texture and naturally sweet flavor. Alternatively, you may choose to slice the banana into rounds for a snack or add it to cereal, yogurt, or smoothies for added nutrition. Remember to dispose of the peel properly, as it can be composted, contributing to environmental sustainability. Enjoy the wholesome benefits of bananas, which are rich in potassium, vitamins, and fiber, making them a perfect on-the-go snack!
"""

in_string4 = """
Peeling a banana is a simple yet essential skill that can enhance the enjoyment of this nutritious fruit. To begin, grasp the banana firmly in one hand, ensuring that the stem end is facing upwards. Using the thumb and forefinger of the opposite hand, gently pinch the stem to create a small opening. This method, often considered easier than peeling from the bottom, allows for a cleaner and more efficient peel. As you pull down the peel in segments, it should separate easily, revealing the soft, sweet fruit inside. Once fully peeled, the banana is ready to be enjoyed as a healthy snack or incorporated into various dishes, such as smoothies, cereals, or baked goods. Proper peeling not only helps maintain the fruit's integrity but also ensures a pleasant eating experience, highlighting the banana's creamy texture and rich flavor.
"""

print(do_text_sim([in_string2, in_string3, in_string4]))


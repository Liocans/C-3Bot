import pandas as pd
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from gensim.models import Word2Vec
import numpy as np

from utilities.path_finder import PathFinder

# Load the data
data = pd.read_csv(PathFinder.get_complet_path('utilities/movie_review.csv'))
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['tag'], test_size=0.2, random_state=42)

# Preprocess the text data
stop_words = set(stopwords.words('english'))
def preprocess(text):
    text = text.lower()
    text = ''.join([word for word in text if word not in string.punctuation])
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

X_train = X_train.apply(preprocess)
X_test = X_test.apply(preprocess)

# Train the Word2Vec model
sentences = [sentence.split() for sentence in X_train]
print(sentences)
w2v_model = Word2Vec(sentences, vector_size=100, window=5, min_count=5, workers=4)

# Vectorize the text data
def vectorize(sentence):
    words = sentence.split()
    words_vecs = [w2v_model.wv[word] for word in words if word in w2v_model.wv]
    if len(words_vecs) == 0:
        return np.zeros(100)
    words_vecs = np.array(words_vecs)
    return words_vecs.mean(axis=0)

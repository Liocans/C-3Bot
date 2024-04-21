import json
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

# Load your intents JSON file
with open('intents.json', 'r') as file:
    data = json.load(file)

sentences = [word_tokenize(" ".join(intent['patterns']).lower()) for intent in data['intents']]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
model.save("word2vec.model")

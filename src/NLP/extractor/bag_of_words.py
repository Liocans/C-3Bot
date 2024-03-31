import os
import json
import numpy as np

from NLP.preprocessing.lemmatizer import Lemmatizer
from NLP.preprocessing.stemmer import Stemmer
from NLP.preprocessing.tokenizer import Tokenizer
from utilities.file_searcher import PathFinder


class BagOfWords:

    def __init__(self, mode="L"):
        self.stemmer = Stemmer()
        self.lemmatizer = Lemmatizer()
        self.tokenizer = Tokenizer()
        self.mode = mode
        self.vocab = []
        self.tags = []
        self.train_x_y = []
        self.bow_representation = None
        self.load_corpus()

    def load_corpus(self):
        filename = PathFinder().get_complet_path('ressources/intents/intents.json')
        # Load intents data from JSON file
        intents_data = None
        with open(filename, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            self.tags.append(intent["tag"])
            for text in intent["texts"]:
                for word in self.preprocess_text(text, intent["tag"], "C"):
                    if word not in self.vocab:
                        self.vocab.append(word)

    def generate_bow(self, sentence):
        self.bow_representation = np.zeros(len(self.vocab))
        for word in sentence if type(sentence) == list else self.preprocess_text(sentence):
            if word in self.vocab:
                index = self.vocab.index(word)
                self.bow_representation[index] += 1
        return self.bow_representation

    def preprocess_text(self, text, tag=None, mode=None):
        tokens = self.tokenizer.tokenize_and_filter_sentence(text)  # Tokenize and convert to lowercase
        if (mode == "C"):
            self.train_x_y.append((tokens, tag))
        return self.lemmatizer.lemmatize(tokens) if self.mode == "L" else self.stemmer.stem_words(tokens)

import json
import numpy as np

from NLP.preprocessing.text_preprocessor import TextPreprocessor
from utilities.file_searcher import PathFinder


class BagOfWords:

    def __init__(self, prepocessor: TextPreprocessor):
        self.prepocessor = prepocessor
        self.vocab = []
        self.tags = []
        self.__load_corpus()

    def extract_features(self, sentence: str):
        bow_representation = np.zeros(len(self.vocab))
        for word in self.prepocessor.preprocess_text(text=sentence):
            if word in self.vocab:
                index = self.vocab.index(word)
                bow_representation[index] += 1
        return bow_representation

    def __load_corpus(self):
        filename = PathFinder().get_complet_path(path_to_file='ressources/intents/intents.json')
        with open(filename, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            self.tags.append(intent["tag"])
            for text in intent["texts"]:
                for word in self.prepocessor.preprocess_text(text=text):
                    if word not in self.vocab:
                        self.vocab.append(word)

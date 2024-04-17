import json

import numpy as np

from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder


class BagOfWords:

    def __init__(self, preprocessor: Preprocessor):
        self.__preprocessor = preprocessor
        self.__vocab = []
        self.__tags = []
        self.__load_corpus()

    def extract_features(self, sentence: str):
        bow_representation = np.zeros(len(self.__vocab))
        for word in self.__preprocessor.preprocess_text(text=sentence):
            if word in self.__vocab:
                index = self.__vocab.index(word)
                bow_representation[index] += 1
        return bow_representation

    def __load_corpus(self):
        file_path = PathFinder().get_complet_path(path_to_file='ressources/json_files/intents.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            self.__tags.append(intent["tag"])
            for text in intent["patterns"]:
                for word in self.__preprocessor.preprocess_text(text=text):
                    if word not in self.__vocab:
                        self.__vocab.append(word)
    @property
    def vocab(self) -> list:
        return self.__vocab

    @property
    def tags(self) -> list:
        return self.__tags

    @property
    def extractor_name(self) -> str:
        return "BagOfWords"

    @property
    def preprocessor(self) -> Preprocessor:
        return self.__preprocessor
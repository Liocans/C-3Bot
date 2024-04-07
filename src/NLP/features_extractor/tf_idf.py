import json
import numpy as np
import math
from collections import defaultdict
from NLP.preprocessing.preprocessor import Preprocessor
from utilities.file_searcher import PathFinder


class TFIDF:
    def __init__(self, prepocessor: Preprocessor):
        self.__prepocessor = prepocessor
        self.__vocab = []
        self.__tags = []
        self.__docs = []  # Store preprocessed documents
        self.__doc_freq = defaultdict(int)  # Document frequency for each word
        self.__load_corpus()
        self.__calculate_doc_freq()

    def extract_features(self, sentence):
        # Preprocess the sentence
        preprocessed_sentence = self.__prepocessor.preprocess_text(sentence)
        # Calculate TF-IDF for each word in the sentence
        tf_idf_vector = np.zeros(len(self.__vocab))
        for word in preprocessed_sentence:
            if word in self.__vocab:
                tf = preprocessed_sentence.count(word) / len(preprocessed_sentence)
                idf = math.log(len(self.__docs) / (1 + self.__doc_freq[word]))
                tf_idf_vector[self.__vocab.index(word)] = tf * idf
        return tf_idf_vector

    def __load_corpus(self):
        file_path = PathFinder.get_complet_path('resources/intents/intents.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            self.__tags.append(intent["tag"])
            for text in intent["texts"]:
                preprocessed_text = self.__prepocessor.preprocess_text(text)
                self.__docs.append(preprocessed_text)
                for word in preprocessed_text:
                    if word not in self.__vocab:
                        self.__vocab.append(word)

    def __calculate_doc_freq(self):
        # Calculate document frequency for each word in the vocabulary
        for doc in self.__docs:
            for word in doc:
                self.__doc_freq[word] += 1

    @property
    def vocab(self) -> list:
        return self.__vocab

    @property
    def tags(self) -> list:
        return self.__tags

import json
import math
from collections import defaultdict

import numpy as np

from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder


class TFIDF:
    def __init__(self, preprocessor: Preprocessor, vocab: list, docs: list):
        self.__preprocessor = preprocessor
        self.__vocab = vocab
        self.__docs = docs  # Store preprocessed documents
        self.__doc_freq = defaultdict(int)  # Document frequency for each word
        self.__calculate_doc_freq()

    def extract_features(self, sentence) -> list:
        # Preprocess the sentence
        preprocessed_sentence = self.__preprocessor.preprocess_text(sentence)
        # Calculate TF-IDF for each word in the sentence
        tf_idf_vector = np.zeros(len(self.__vocab)).tolist()
        for word in preprocessed_sentence:
            if word in self.__vocab:
                tf = preprocessed_sentence.count(word) / len(preprocessed_sentence)
                idf = math.log(len(self.__docs) / (1 + self.__doc_freq[word]))
                tf_idf_vector[self.__vocab.index(word)] = tf * idf
        return tf_idf_vector

    def __calculate_doc_freq(self):
        # Calculate document frequency for each word in the vocabulary
        for doc in self.__docs:
            for word in doc:
                self.__doc_freq[word] += 1


    @property
    def extractor_name(self) -> str:
        return "TFIDF"

    @property
    def preprocessor(self) -> Preprocessor:
        return self.__preprocessor
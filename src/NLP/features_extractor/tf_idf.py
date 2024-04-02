import json
import numpy as np
import math
from collections import defaultdict
from NLP.preprocessing.text_preprocessor import TextPreprocessor
from utilities.file_searcher import PathFinder


class TFIDF:
    def __init__(self, prepocessor: TextPreprocessor):
        self.prepocessor = prepocessor
        self.vocab = []
        self.tags = []
        self.docs = []  # Store preprocessed documents
        self.doc_freq = defaultdict(int)  # Document frequency for each word
        self.__load_corpus()
        self.__calculate_doc_freq()

    def extract_features(self, sentence):
        # Preprocess the sentence
        preprocessed_sentence = self.prepocessor.preprocess_text(sentence)
        # Calculate TF-IDF for each word in the sentence
        tf_idf_vector = np.zeros(len(self.vocab))
        for word in preprocessed_sentence:
            if word in self.vocab:
                tf = preprocessed_sentence.count(word) / len(preprocessed_sentence)
                idf = math.log(len(self.docs) / (1 + self.doc_freq[word]))
                tf_idf_vector[self.vocab.index(word)] = tf * idf
        return tf_idf_vector

    def __load_corpus(self):
        filename = PathFinder().get_complete_path('resources/intents/intents.json')
        with open(filename, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            self.tags.append(intent["tag"])
            for text in intent["texts"]:
                preprocessed_text = self.prepocessor.preprocess_text(text)
                self.docs.append(preprocessed_text)
                for word in preprocessed_text:
                    if word not in self.vocab:
                        self.vocab.append(word)

    def __calculate_doc_freq(self):
        # Calculate document frequency for each word in the vocabulary
        for doc in self.docs:
            for word in doc:
                self.doc_freq[word] += 1


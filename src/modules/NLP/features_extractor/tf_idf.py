import math
from collections import defaultdict

import numpy as np

from modules.NLP.preprocessing.preprocessor import Preprocessor


class TFIDF:
    """
    A class that implements the Term Frequency-Inverse Document Frequency (TF-IDF) model for feature extraction in
    natural language processing. This model measures the importance of a word in a document relative to a corpus,
    producing a weight for each word which is higher when the word is rare across documents but frequent within the
    document itself.

    Attributes:
        __preprocessor (Preprocessor): An instance of the Preprocessor class used for tokenizing and normalizing text.
        __vocab (list): A list of unique words that forms the vocabulary of the corpus.
        __docs (list): A list of preprocessed documents or sentences.
        __doc_freq (defaultdict[int]): A dictionary storing the document frequency of each word in the vocabulary.

    Methods:
        extract_features(sentence: str) -> list:
            Converts a sentence into a vector of TF-IDF scores using the class's vocabulary and document frequencies.
    """

    def __init__(self, preprocessor: Preprocessor, vocab: list, docs: list):

        """
        Initializes the TFIDF class with a specified preprocessor, vocabulary, and a list of preprocessed documents.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use for text preprocessing.
            vocab (list): The vocabulary list, each word of which will be assessed in the documents.
            docs (list): A list of preprocessed documents, which are used to calculate document frequency.
        """

        self.__preprocessor = preprocessor
        self.__vocab = vocab
        self.__docs = docs  # Store preprocessed documents
        self.__doc_freq = defaultdict(int)  # Document frequency for each word
        self.__calculate_doc_freq()

    def extract_features(self, sentence: str) -> np.ndarray:
        """
        Extracts the TF-IDF vector for a given sentence based on the class's vocabulary and document frequency data.

        Parameters:
            sentence (str): The sentence to convert into a TF-IDF vector.

        Returns:
            list: A list of TF-IDF scores corresponding to the vocabulary indices.
        """

        # Preprocess the sentence
        preprocessed_sentence = self.__preprocessor.preprocess_text(sentence)
        # Calculate TF-IDF for each word in the sentence
        tf_idf_vector = np.zeros(len(self.__vocab))
        for word in preprocessed_sentence:
            if word in self.__vocab:
                tf = preprocessed_sentence.count(word) / len(preprocessed_sentence)
                idf = math.log(len(self.__docs) / (1 + self.__doc_freq[word]))
                tf_idf_vector[self.__vocab.index(word)] = tf * idf
        return tf_idf_vector

    def __calculate_doc_freq(self) -> None:
        """
        Calculates the document frequency for each word in the vocabulary based on the provided documents.
        Document frequency is incremented once for each word per document if the word is present.
        """

        # Calculate document frequency for each word in the vocabulary
        for doc in self.__docs:
            for word in doc:
                self.__doc_freq[word] += 1

    @property
    def extractor_name(self) -> str:
        """
        Retrieves the name of the current feature extractor.

        Returns:
            str: The name of the feature extractor, "TFIDF".
        """

        return "TFIDF"

    @property
    def preprocessor(self) -> Preprocessor:
        """
        Accesses the preprocessor used in the TF-IDF model.

        Returns:
            Preprocessor: The preprocessor instance used for preparing text data.
        """

        return self.__preprocessor

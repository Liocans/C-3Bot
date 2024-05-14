import numpy as np

from modules.NLP.preprocessing.preprocessor import Preprocessor


class BagOfWords:
    """
    A class that implements the Bag of Words (BoW) model for feature extraction in natural language processing.
    This model transforms text into a fixed-length vector of integers, where each index represents a word
    from the corpus and each value represents the frequency of the corresponding word in a given text.

    Attributes:
        __preprocessor (Preprocessor): An instance of the Preprocessor class used for tokenizing and normalizing text.
        __vocab (list): A list of unique words that forms the vocabulary of the corpus.
    """

    def __init__(self, preprocessor: Preprocessor, vocab: list):
        """
        Initializes the BagOfWords class with a specified preprocessor.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use for text preprocessing.
            vocab (list): The vocabulary list, each word of which will be represented in the feature vectors.
        """

        self.__preprocessor = preprocessor
        self.__vocab = vocab

    def extract_features(self, sentence: str) -> np.ndarray:
        """
        Converts a sentence into a bag-of-words vector using the class's vocabulary.

        Parameters:
            sentence (str): The sentence to convert into a bag-of-words representation.

        Returns:
            np.ndarray: A numpy array representing the sentence as a vector of word frequencies.
        """

        bow_representation = np.zeros(len(self.__vocab))
        for word in self.__preprocessor.preprocess_text(text=sentence):
            if word in self.__vocab:
                index = self.__vocab.index(word)
                bow_representation[index] += 1
        return bow_representation

    @property
    def extractor_name(self) -> str:
        """
        Returns the name of the feature extractor.

        Returns:
            str: The name of the feature extractor, "BagOfWords".
        """

        return "BagOfWords"

    @property
    def preprocessor(self) -> Preprocessor:
        """
        Accesses the preprocessor used in the Bag of Words model.

        Returns:
            Preprocessor: The preprocessor instance used for preparing text data.
        """

        return self.__preprocessor

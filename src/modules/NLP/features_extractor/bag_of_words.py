import json

import numpy as np

from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder


class BagOfWords:
    """
    A class that implements the Bag of Words (BoW) model for feature extraction in natural language processing.
    This model transforms text into a fixed-length vector of integers, where each index represents a word
    from the corpus and each value represents the frequency of the corresponding word in a given text.

    Attributes:
        __preprocessor (Preprocessor): An instance of the Preprocessor class used for tokenizing and normalizing text.
        __vocab (list): A list of unique words that forms the vocabulary of the corpus.
        __tags (list): A list of tags or categories associated with different intents or purposes in the corpus.
    """
    def __init__(self, preprocessor: Preprocessor):
        """
        Initializes the BagOfWords class with a specified preprocessor.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use for text preprocessing.
        """
        self.__preprocessor = preprocessor
        self.__vocab = []
        self.__tags = []
        self.__load_corpus()

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

    def __load_corpus(self) -> None:
        """
        Loads the training data from a JSON file and builds the vocabulary and tags list based on the
        preprocessed text of the training data.
        """
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
        """
        Retrieves the vocabulary of the corpus.

        Returns:
            list: A list of unique words that make up the vocabulary.
        """
        return self.__vocab

    @property
    def tags(self) -> list:
        """
        Retrieves the tags or categories associated with the corpus.

        Returns:
            list: A list of tags associated with different intents or purposes.
        """
        return self.__tags

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

import json
import numpy as np

from gensim.models import Word2Vec as GensimWord2Vec
from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder

class Word2Vec:
    """
    A class that implements the Word2Vec model for feature extraction in natural language processing.
    This model transforms text into vectors using a neural network architecture that learns to predict
    context words from target words or vice versa.

    Attributes:
        __preprocessor (Preprocessor): An instance of the Preprocessor class used for tokenizing and normalizing text.
        __model (GensimWord2Vec): A Gensim Word2Vec model instance.
    """
    def __init__(self, preprocessor: Preprocessor, vocab: list, docs: list, vector_size=100, window=5, min_count=1, workers=4):
        """
        Initializes the Word2Vec class with a specified preprocessor and Word2Vec parameters.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use for text preprocessing.
            vector_size (int): Dimensionality of the word vectors.
            window (int): Maximum distance between the current and predicted word.
            min_count (int): Ignores all words with total frequency lower than this.
            workers (int): Number of worker threads to train the model.
        """
        self.__preprocessor = preprocessor
        self.__model = None
        self.__tags = vocab
        self.__docs = docs
        self.__train(vector_size, window, min_count, workers)

    def extract_features(self, sentence: str) -> list:
        """
        Converts a sentence into a vector by averaging the vectors of the words in the sentence.

        Parameters:
            sentence (str): The sentence to convert.

        Returns:
            np.ndarray: A numpy array representing the sentence as a vector.
        """
        words = self.__preprocessor.preprocess_text(text=sentence)
        sentence_vector = [self.get_word_vector(word) for word in words if word in self.__model.wv]
        if len(sentence_vector) != 0:
            sentence_vector = np.array(sentence_vector).mean(axis=0).tolist()
        else:
            sentence_vector = np.zeros(self.__model.vector_size).tolist()
        return sentence_vector

    def get_word_vector(self, word: str) -> np.ndarray:
        """
        Retrieves the vector representation of a word.

        Parameters:
            word (str): The word to retrieve the vector for.

        Returns:
            np.ndarray: A numpy array representing the word's vector.
        """

        return self.__model.wv[word] if word in self.__model.wv else np.zeros(self.__model.vector_size)

    def __train(self, vector_size, window, min_count, workers):

        # Initialize and train the Word2Vec model
        self.__model = GensimWord2Vec(self.__docs, vector_size=vector_size, window=window, min_count=min_count,
                                      workers=workers)

    @property
    def extractor_name(self) -> str:
        """
        Returns the name of the feature extractor.

        Returns:
            str: The name of the feature extractor, "Word2Vec".
        """
        return "Word2Vec"

    @property
    def preprocessor(self) -> Preprocessor:
        """
        Accesses the preprocessor used in the Bag of Words model.

        Returns:
            Preprocessor: The preprocessor instance used for preparing text data.
        """
        return self.__preprocessor

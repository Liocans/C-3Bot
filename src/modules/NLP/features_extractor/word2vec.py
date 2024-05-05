import numpy as np

from gensim.models import Word2Vec as GensimWord2Vec
from modules.NLP.preprocessing.preprocessor import Preprocessor


class Word2Vec:
    """
    A class that implements the Word2Vec model for feature extraction in natural language processing.
    This model transforms text into vectors using a neural network architecture that learns to predict
    context words from target words or vice versa.

    Attributes:
        __preprocessor (Preprocessor): An instance of the Preprocessor class used for tokenizing and normalizing text.
        __model (GensimWord2Vec): A Gensim Word2Vec model instance.
    """

    def __init__(self, preprocessor: Preprocessor, docs: list, vector_size=100, window=5, min_count=1, workers=4, sg=0):
        """
        Initializes the Word2VecExtractor class with a specified preprocessor and parameters for constructing the Word2Vec model.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use for text preprocessing.
            docs (list): A list of tokenized documents/sentences for training the model.
            vector_size (int): Dimensionality of the word vectors.
            window (int): Maximum distance between the current and predicted word within a sentence.
            min_count (int): Ignores all words with total frequency lower than this.
            workers (int): Number of worker threads to train the model.
            sg (int): Training algorithm: 1 for skip-gram; otherwise CBOW.
        """
        self.__preprocessor = preprocessor
        self.__model = None
        self.__docs = docs
        self.__train(vector_size, window, min_count, workers, sg)

    def extract_features(self, sentence: str) -> np.ndarray:
        """
        Converts a sentence into a vector by averaging the vectors of the words in the sentence.

        Parameters:
            sentence (str): The sentence to convert.

        Returns:
            np.ndarray: A numpy array representing the sentence as a vector, averaging the vectors of the words in the sentence.
        """

        words = self.__preprocessor.preprocess_text(text=sentence)
        sentence_vector = [self.__get_word_vector(word) for word in words if word in self.__model.wv]
        if len(sentence_vector) != 0:
            sentence_vector = np.array(sentence_vector).mean(axis=0)
        else:
            sentence_vector = np.zeros(self.__model.vector_size)
        return sentence_vector

    def __get_word_vector(self, word: str) -> np.ndarray:
        """
        Retrieves the vector representation of a word, if it exists in the model's vocabulary.

        Parameters:
            word (str): The word to retrieve the vector for.

        Returns:
            np.ndarray: A numpy array representing the word's vector, or a zero vector if the word is not in the vocabulary.
        """

        return self.__model.wv[word] if word in self.__model.wv else np.zeros(self.__model.vector_size)

    def __train(self, vector_size, window, min_count, workers, sg):
        """
        Initializes and trains the Word2Vec model using the specified parameters and the provided documents.

        Parameters:
            vector_size (int): The dimensionality of the word vectors.
            window (int): The maximum distance between the current and predicted word within a sentence.
            min_count (int): The minimum count of words considered when training the model.
            workers (int): The number of worker threads to use in training.
            sg (int): Specifies the training algorithm: 1 for skip-gram, otherwise CBOW.
        """
        # Initialize and train the Word2Vec model
        self.__model = GensimWord2Vec(self.__docs, vector_size=vector_size, window=window, min_count=min_count,
                                workers=workers, sg=sg)

    @property
    def extractor_name(self) -> str:
        """
        Returns the name of the feature extractor used, which is "Word2Vec".

        Returns:
            str: The name of the feature extractor, "Word2Vec".
        """
        return "Word2Vec"

    @property
    def preprocessor(self) -> Preprocessor:
        """
        Accesses the preprocessor used in the Word2Vec model.

        Returns:
            Preprocessor: The preprocessor instance used for preparing text data.
        """
        return self.__preprocessor

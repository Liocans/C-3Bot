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

    def __init__(self, preprocessor: Preprocessor, docs: list, vector_size: int = 100, window: int = 5,
                 min_count: int = 1, workers: int = 4, sg: int = 0):
        """
        Initializes the Word2Vec class with a specified preprocessor and parameters for the Word2Vec model construction.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance for text preprocessing.
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
        self.__vector_size = vector_size
        self.__window = window
        self.__min_count = min_count
        self.__workers = workers
        self.__sg = sg

    def extract_features(self, sentence: str) -> np.ndarray:
        """
        Converts a sentence into a vector by averaging the vectors of the words present in the sentence, processed through the model.

        Parameters:
            sentence (str): The sentence to convert.

        Returns:
            np.ndarray: A numpy array representing the sentence as a vector, averaging the vectors of the words in the sentence.
        """

        words = self.__preprocessor.preprocess_text(text=sentence)
        sentence_vector = np.zeros(self.__vector_size)
        for word in words:
            if word in self.__model.wv:
                sentence_vector += self.__model.wv[word]
        sentence_vector /= len(words)
        return sentence_vector

    def __get_word_vector(self, word: str) -> np.ndarray:
        """
        Retrieves the vector representation of a word from the model's vocabulary.

        Parameters:
            word (str): The word for which to retrieve the vector.

        Returns:
            np.ndarray: The vector representation of the word, or a zero vector if the word is not in the vocabulary.
        """

        return self.__model.wv[word] if word in self.__model.wv else np.zeros(self.__model.vector_size)

    def train(self, model_name: str) -> None:
        """
        Initializes and trains the Word2Vec model using the provided documents, then saves the trained model.

        Parameters:
            model_name (str): The name to use for saving the trained model file.
        """

        self.__model = GensimWord2Vec(self.__docs, vector_size=self.__vector_size, window=self.__window,
                                      min_count=self.__min_count, workers=self.__workers, sg=self.__sg)

        self.__save_model(model_name)

    def __save_model(self, model_name: str) -> None:
        """
        Saves the trained Word2Vec model to the specified file path.

        Parameters:
            model_name (str): The name of the model to be saved.
        """

        file_path = PathFinder.get_complet_path(f"ressources/extractors/{model_name}_E.pth")
        self.__model.save(file_path)

    def load_model(self, model_name: str) -> None:
        """
        Loads a Word2Vec model from the specified file path.

        Parameters:
            model_name (str): The name of the model to be loaded.
        """
        model_name = model_name.replace(".pth", "")
        file_path = PathFinder.get_complet_path(f"ressources/extractors/{model_name}_E.pth")
        self.__model = GensimWord2Vec.load(file_path)

    @property
    def extractor_name(self) -> str:
        """
        Returns the name of the feature extractor used, which is "Word2Vec_CBOW" or "Word2Vec_GRAM".

        Returns:
            str: The name of the feature extractor, "Word2Vec_CBOW" or "Word2Vec_GRAM" .
        """

        return "Word2Vec_CBOW" if self.__sg == 0 else "Word2Vec_GRAM"

    @property
    def preprocessor(self) -> Preprocessor:
        """
        Accesses the preprocessor used in the Word2Vec model.

        Returns:
            Preprocessor: The preprocessor instance used for preparing text data.
        """

        return self.__preprocessor

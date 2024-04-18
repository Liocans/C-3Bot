from modules.NLP.features_extractor.bag_of_words import BagOfWords
from modules.NLP.features_extractor.tf_idf import TFIDF
from modules.NLP.preprocessing.preprocessor import Preprocessor


class Extractor:
    """
    A flexible class that handles feature extraction for text processing tasks by utilizing different feature
    extraction strategies like Bag of Words or TF-IDF, depending on configuration.

    Attributes:
        __preprocessor (Preprocessor): An instance of the Preprocessor class used for text preprocessing.
        __extractor_name (str): The name of the feature extractor currently in use.
        __extractor (BagOfWords | TFIDF): The feature extractor object, which can be either a BagOfWords or TFIDF instance.

    Methods:
        extract_features(sentence): Extracts features from a given sentence using the configured feature extractor.
    """
    def __init__(self, preprocessor: Preprocessor, extractor_name: str = "BagOfWords"):
        """
        Initializes the Extractor class with a specified preprocessor and extractor type.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use for preparing text data.
            extractor_name (str, optional): The type of feature extractor to use. Defaults to "BagOfWords".
        """
        self.__preprocessor = preprocessor
        self.__extractor_name = extractor_name
        self.__extractor = self.__select_extractor(preprocessor=preprocessor, extractor_name=extractor_name)

    def extract_features(self, sentence: str) -> list:
        """
        Extracts features from a given sentence using the selected feature extraction method.

        Parameters:
            sentence (str): The sentence from which to extract features.

        Returns:
            list: A list of features extracted from the sentence.
        """
        return self.__extractor.extract_features(sentence)

    def __select_extractor(self, preprocessor, extractor_name) -> BagOfWords | TFIDF:
        """
        Selects the feature extractor based on the provided extractor name.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use with the feature extractor.
            extractor_name (str): The name of the extractor to use.

        Returns:
            BagOfWords | TFIDF: An instance of the specified feature extractor, initialized with the given preprocessor.
        """
        if extractor_name == "BagOfWords":
            return BagOfWords(preprocessor=preprocessor)
        elif extractor_name == "TFIDF":
            return TFIDF(preprocessor=preprocessor)

    @property
    def vocab(self) -> list:
        """
        Accesses the vocabulary used by the current feature extractor.

        Returns:
            list: The vocabulary list from the current feature extractor.
        """
        return self.__extractor.vocab

    @property
    def tags(self) -> list:
        """
        Accesses the tags or categories used by the current feature extractor.

        Returns:
            list: A list of tags from the current feature extractor.
        """
        return self.__extractor.tags

    @property
    def extractor_name(self) -> str:
        """
        Retrieves the name of the current feature extractor.

        Returns:
            str: The name of the current feature extractor.
        """
        return self.__extractor_name

    @property
    def preprocessor(self) -> Preprocessor:
        """
        Retrieves the preprocessor associated with the current feature extractor.

        Returns:
            Preprocessor: The preprocessor instance being used.
        """
        return self.__preprocessor

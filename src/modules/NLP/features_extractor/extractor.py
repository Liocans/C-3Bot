import json

import numpy as np

from modules.NLP.features_extractor.bag_of_words import BagOfWords
from modules.NLP.features_extractor.tf_idf import TFIDF
from modules.NLP.features_extractor.word2vec import Word2Vec
from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder


class Extractor:
    """
    A flexible class designed for feature extraction in natural language processing tasks. It supports various feature
    extraction techniques like Bag of Words, TF-IDF, and Word2Vec, which can be configured dynamically.

    Attributes:
        __preprocessor (Preprocessor): An instance used for text preprocessing.
        __extractor (Union[BagOfWords, TFIDF, Word2Vec]): The feature extractor object, which can be an instance of
        BagOfWords, TFIDF, or Word2Vec depending on configuration.

    Methods:
        extract_features(sentence: str) -> list:
            Extracts features from a given sentence using the configured feature extractor.
    """

    def __init__(self, preprocessor: Preprocessor, extractor_name: str = "BagOfWords", vocab: list = None,
                 tags: list = None, docs: list = None, window: int = None, vector_size: int = None,
                 model_name: str = None, is_training: bool = False):
        """
        Initializes the Extractor class with specified configurations for text preprocessing and feature extraction.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use for text preprocessing.
            extractor_name (str): The type of feature extractor to use. Defaults to "BagOfWords".
            vocab (list): A list of vocabulary words relevant for some extractors.
            tags (list): A list of tags or categories used in the model.
            docs (list): A list of documents or sentences used primarily with Word2Vec.
            window (int): The maximum distance between the current and predicted word in a Word2Vec model.
            vector_size (int): The dimensionality of the word vectors in a Word2Vec model.
        """

        self.__vocab = vocab
        self.__docs = docs
        self.__tags = tags
        self.__preprocessor = preprocessor
        self.__extractor = None
        self.__is_training = is_training
        self.__select_extractor(preprocessor=preprocessor, extractor_name=extractor_name,
                                window=window, vector_size=vector_size, model_name=model_name)

    def extract_features(self, sentence: str) -> np.ndarray:
        """
        Extracts features from a given sentence using the selected feature extraction method, returning a list of features.

        Parameters:
            sentence (str): The sentence from which to extract features.

        Returns:
            list: A list of features extracted from the sentence.
        """

        return self.__extractor.extract_features(sentence)

    def __select_extractor(self, preprocessor, extractor_name, window, vector_size, model_name) -> None:
        """
        Selects the appropriate feature extractor based on the provided extractor name and initializes it.

        Parameters:
            preprocessor (Preprocessor): The preprocessor instance to use with the feature extractor.
            extractor_name (str): The name of the extractor to use.

        Returns:
            Union[BagOfWords, TFIDF, Word2Vec]: An instance of the specified feature extractor, initialized with the given parameters.
        """

        if self.__vocab == self.__docs == self.__tags is None:
            self.__load_corpus()

        if extractor_name == "BagOfWords":
            self.__extractor = BagOfWords(preprocessor=preprocessor, vocab=self.__vocab)

        elif extractor_name == "TFIDF":
            self.__extractor = TFIDF(preprocessor=preprocessor, vocab=self.__vocab, docs=self.__docs)

        elif extractor_name in ["Word2Vec_CBOW", "Word2Vec_GRAM"]:
            sg = 0 if extractor_name == "Word2Vec_CBOW" else 1
            self.__extractor = Word2Vec(preprocessor=preprocessor, docs=self.__docs, window=window,
                                        vector_size=vector_size, sg=sg)
            if self.__is_training:
                print("training WORD2VEC")
                self.__extractor.train(model_name=model_name)
            else:
                print("loading WORD2VEC")
                self.__extractor.load_model(model_name=model_name)

    def __load_corpus(self):
        """
        Loads the corpus data from a JSON file and extracts vocabulary, documents, and tags to be used in the model.
        """

        self.__tags = []
        self.__docs = []
        self.__vocab = []
        file_path = PathFinder.get_complet_path('ressources/json_files/intents.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            self.__tags.append(intent["tag"])
            for text in intent["patterns"]:
                preprocessed_text = self.__preprocessor.preprocess_text(text)
                self.__docs.append(preprocessed_text)
                for word in preprocessed_text:
                    if word not in self.__vocab:
                        self.__vocab.append(word)

    @property
    def vocab(self) -> list:
        """
        Accesses the vocabulary.

        Returns:
            list: The vocabulary list.
        """

        return self.__vocab

    @property
    def tags(self) -> list:
        """
        Accesses the tags.

        Returns:
            list: A list of tags.
        """

        return self.__tags

    @property
    def docs(self) -> list:
        """
        Accesses the docs.

        Returns:
            list: A list of all the document.
        """

        return self.__docs

    @property
    def extractor_name(self) -> str:
        """
        Retrieves the name of the current feature extractor.

        Returns:
            str: The name of the current feature extractor.
        """

        return self.__extractor.extractor_name

    @property
    def preprocessor(self) -> Preprocessor:
        """
        Retrieves the preprocessor associated with the current feature extractor.

        Returns:
            Preprocessor: The preprocessor instance being used.
        """

        return self.__extractor.preprocessor

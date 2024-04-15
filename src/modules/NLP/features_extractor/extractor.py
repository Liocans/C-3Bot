from modules.NLP.features_extractor.bag_of_words import BagOfWords
from modules.NLP.features_extractor.tf_idf import TFIDF
from modules.NLP.preprocessing.preprocessor import Preprocessor


class Extractor:
    def __init__(self, preprocessor: Preprocessor, extractor_name="BagOfWords"):
        self.__preprocessor = preprocessor
        self.__extractor_name = extractor_name
        self.__extractor = self.__select_extractor(preprocessor=preprocessor, extractor_name=extractor_name)

    def extract_features(self, sentence: str) -> list:
        return self.__extractor.extract_features(sentence)

    def __select_extractor(self, preprocessor, extractor_name):
        if extractor_name == "BagOfWords":
            return BagOfWords(preprocessor=preprocessor)
        elif extractor_name == "TFIDF":
            return TFIDF(preprocessor=preprocessor)

    @property
    def vocab(self) -> list:
        return self.__extractor.vocab

    @property
    def tags(self) -> list:
        return self.__extractor.tags

    @property
    def extractor_name(self) -> str:
        return self.__extractor_name

    @property
    def preprocessor(self) -> Preprocessor:
        return self.__preprocessor

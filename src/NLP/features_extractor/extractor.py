from NLP.features_extractor.bag_of_words import BagOfWords
from NLP.features_extractor.tf_idf import TFIDF
from NLP.preprocessing.preprocessor import Preprocessor


class Extractor:
    def __init__(self, prepocessor: Preprocessor, extractor_name="BagOfWords"):
        self.__extractor = self.__select_extractor(preprocessor=prepocessor, extractor_name=extractor_name)

    def extract_features(self, sentence: str) -> list:
        return self.__extractor.extract_features(sentence)

    def __select_extractor(self, preprocessor, extractor_name):
        if extractor_name == "BagOfWords":
            return BagOfWords(prepocessor=preprocessor)
        elif extractor_name == "TFIDF":
            return TFIDF(prepocessor=preprocessor)

    @property
    def vocab(self) -> list:
        return self.__extractor.vocab

    @property
    def tags(self) -> list:
        return self.__extractor.tags

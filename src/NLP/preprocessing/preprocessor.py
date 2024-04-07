from NLP.preprocessing.lemmatizer import Lemmatizer
from NLP.preprocessing.stemmer import Stemmer
from NLP.preprocessing.tokenizer import Tokenizer


class Preprocessor:
    def __init__(self, preprocessor_name="Lemmatizer", remove_stopwords: bool = False):
        self.__preprocessor = self.__select_preprocessor(preprocessor_name=preprocessor_name)
        self.__tokinizer = Tokenizer(exclude_stopwords=remove_stopwords)

    def preprocess_text(self, text: str) -> list:
        tokens = self.__tokinizer.tokenize_and_filter_sentence(text)  # Tokenize and convert to lowercase
        return self.__preprocessor.preprocess_text(tokens)

    def __select_preprocessor(self, preprocessor_name):
        if preprocessor_name == "Stemmer":
            return Stemmer()
        elif preprocessor_name == "Lemmatizer":
            return Lemmatizer()

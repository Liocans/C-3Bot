from NLP.preprocessing.lemmatizer import Lemmatizer
from NLP.preprocessing.stemmer import Stemmer
from NLP.preprocessing.tokenizer import Tokenizer


class TextPreprocessor:
    def __init__(self, mode: str = 'L', remove_stopwords: bool = False):
        self.__lemmatizer = Lemmatizer()
        self.__stemmer = Stemmer()
        self.__tokinizer = Tokenizer(exclude_stopwords=remove_stopwords)
        self.__mode = mode

    def preprocess_text(self, text: str) -> list:
        tokens = self.__tokinizer.tokenize_and_filter_sentence(text)  # Tokenize and convert to lowercase
        return self.__lemmatizer.lemmatize(tokens) if self.__mode == 'L' else self.__stemmer.stem_words(tokens)

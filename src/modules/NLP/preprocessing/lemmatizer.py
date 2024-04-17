import nltk
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

class Lemmatizer:

    def __init__(self):
        self.__lemmatizer = WordNetLemmatizer()

    def __get_wordnet_pos(self, tag: str) -> str:
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def preprocess_text(self, tokens: list) -> list:
        pos_tags = pos_tag(tokens)
        lemmatized_words = [self.__lemmatizer.lemmatize(word, self.__get_wordnet_pos(tag)) for word, tag in pos_tags]
        return lemmatized_words

    @property
    def preprocessor_name(self) -> str:
        return "Lemmatizer"

    @property
    def remove_stopwords(self) -> bool:
        return self.__remove_stopwords

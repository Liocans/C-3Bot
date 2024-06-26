import nltk
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


class Lemmatizer:
    """
    A class that encapsulates the functionality of word lemmatization using NLTK's WordNetLemmatizer.
    It processes lists of tokens and applies part-of-speech tagging and lemmatization to each token.

    Attributes:
        __lemmatizer (WordNetLemmatizer): An instance of NLTK's WordNetLemmatizer.

    Methods:
        preprocess_text(tokens): Lemmatizes a list of tokens based on their part-of-speech tags.
        preprocessor_name: Returns the name of the preprocessor as 'Lemmatizer'.
    """

    def __init__(self):
        """
        Initializes the Lemmatizer class by creating an instance of the WordNetLemmatizer.
        """
        self.__lemmatizer = WordNetLemmatizer()

    def __get_wordnet_pos(self, tag: str) -> str:
        """
        Determines the WordNet part-of-speech tag based on the simple POS tag generated by NLTK's pos_tag.

        Parameters:
            tag (str): The part-of-speech tag provided by NLTK's pos_tag function.

        Returns:
            str: A WordNet part-of-speech tag corresponding to the input tag.
        """
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
        """
        Lemmatizes a list of tokens based on their part-of-speech tags to their base or dictionary form.

        Parameters:
            tokens (list): A list of word tokens to be lemmatized.

        Returns:
            list: A list of lemmatized word tokens.
        """
        pos_tags = pos_tag(tokens)
        lemmatized_words = [self.__lemmatizer.lemmatize(word, self.__get_wordnet_pos(tag)) for word, tag in pos_tags]
        return lemmatized_words

    @property
    def preprocessor_name(self) -> str:
        """
        A property to get the name of the preprocessor.

        Returns:
            str: The name of this preprocessor, 'Lemmatizer'.
        """
        return "Lemmatizer"

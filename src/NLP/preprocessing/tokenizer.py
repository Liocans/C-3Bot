import re
import string
import os

from utilities.file_searcher import PathFinder


class Tokenizer:
    """
    A tokenizer class that processes and tokenizes input sentences.

    This class provides functionality to tokenize sentences into words, optionally excluding
    stopwords, and removing punctuation from the input sentence.
    """

    def __init__(self, exclude_stopwords: bool = True):
        """
        Initializes the Tokenizer instance.

        Parameters:
            exclude_stopwords (bool): If True, stopwords will be excluded from the tokenized output.
                                      Defaults to True.
        """

        self.__stop_words = self.__load_stop_words()
        self.__exclude_stopwords = exclude_stopwords

    def tokenize_and_filter_sentence(self, sentence: str) -> list:
        """
        Tokenizes the input sentence and filters it according to the instance's configuration.

        This method removes punctuation from the input sentence, tokenizes it, and optionally
        removes stopwords from the list of tokens.

        Parameters:
            sentence (str): The sentence to tokenize and filter.

        Returns:
            list: A list of tokens derived from the input sentence.
        """

        sentence = self.__remove_punctuation(sentence=sentence)
        tokens = self.__tokenize(sentence=sentence)
        if (not self.__exclude_stopwords):
            tokens = self.__remove_stop_words(tokens=tokens)
        return tokens

    def __load_stop_words(self) -> set:
        """
        Loads and returns a set of stopwords.

        This method reads stopwords from a specified file and returns them as a set.

        Returns:
            set: A set of stopwords.
        """

        stop_words = set()
        file_path = PathFinder().get_complet_path(path_to_file="ressources/stop_words/english.txt")

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                stop_words.add(line.strip())
        return stop_words

    def __tokenize(self, sentence: str) -> list:
        """
        Tokenizes the input sentence into a list of words.

        This method applies a regular expression pattern to find all tokens in the input sentence.

        Parameters:
            sentence (str): The sentence to tokenize.

        Returns:
            list: A list of tokens found in the input sentence.
        """

        pattern = r'\w+|\$[\d\.]+|\S+'
        tokens = re.findall(pattern, sentence.lower())
        return tokens

    def __remove_stop_words(self, tokens: list) -> list:
        """
        Removes stopwords from the list of tokens.

        Parameters:
            tokens (list): The list of tokens from which to remove stopwords.

        Returns:
            list: A list of tokens with stopwords removed.
        """

        filtered_words = [word for word in tokens if word not in self.__stop_words]
        return filtered_words

    def __remove_punctuation(self, sentence: str) -> str:
        """
        Removes punctuation from the input sentence.

        Parameters:
            sentence (str): The sentence from which to remove punctuation.

        Returns:
            str: The input sentence with punctuation removed.
        """

        translator = str.maketrans('', '', string.punctuation)
        return sentence.translate(translator)

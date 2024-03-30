import re
import string
import os

from utilities.file_searcher import PathFinder


class Tokenizer:
    def __init__(self, language="english"):
        self.__language = language
        self.__stop_words = self.__load_stop_words()

    def tokenize_and_filter_sentence(self, sentence: str, exclude_stopwords=True) -> list:
        sentence = self.__remove_punctuation(sentence)
        tokens = self.__tokenize(sentence)
        if (not exclude_stopwords):
            tokens = self.__remove_stop_words(tokens)
        return tokens

    def __load_stop_words(self) -> set:
        stop_words = set()
        file_path = PathFinder().get_complet_path(f"ressources/stop_words/{self.__language}.txt")

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                stop_words.add(line.strip())
        return stop_words

    def __tokenize(self, sentence: str) -> list:
        pattern = r'\w+|\$[\d\.]+|\S+'
        tokens = re.findall(pattern, sentence.lower())
        return tokens

    def __remove_stop_words(self, tokens: list) -> list:
        filtered_words = [word for word in tokens if word not in self.__stop_words]
        return filtered_words

    def __remove_punctuation(self, sentence: str) -> str:
        translator = str.maketrans('', '', string.punctuation)
        return sentence.translate(translator)

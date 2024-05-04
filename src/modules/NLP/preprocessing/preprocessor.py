from modules.NLP.preprocessing.lemmatizer import Lemmatizer
from modules.NLP.preprocessing.stemmer import Stemmer
from modules.NLP.preprocessing.tokenizer import Tokenizer


class Preprocessor:
    """
    A class that encapsulates text preprocessing functionalities, including tokenization, stemming, and lemmatization.
    Depending on the specified preprocessing strategy, it either lemmatizes or stems the input text, with the option
    to remove stopwords during tokenization.

    Attributes:
        __preprocessor_name (str): The name of the preprocessor to use, either "Lemmatizer" or "Stemmer".
        __remove_stopwords (bool): Flag indicating whether to remove stopwords during tokenization.
        __preprocessor (Stemmer | Lemmatizer): The preprocessing object, either a Stemmer or Lemmatizer instance.
        __tokenizer (Tokenizer): The tokenizer instance, configured to optionally exclude stopwords.

    Methods:
        preprocess_text(text): Processes the input text using the selected preprocessing method and tokenizer.
        preprocessor_name: Property that returns the name of the current preprocessor.
        remove_stopwords: Property that indicates whether stopwords are removed during tokenization.
    """

    def __init__(self, preprocessor_name:str="Lemmatizer", remove_stopwords: bool = False):
        """
        Initializes the Preprocessor class with a specified preprocessor and configuration for stopwords.

        Parameters:
            preprocessor_name (str, optional): The name of the preprocessor to use. Defaults to "Lemmatizer".
            remove_stopwords (bool, optional): Specifies whether to remove stopwords during tokenization. Defaults to False.
        """
        self.__preprocessor_name = preprocessor_name
        self.__remove_stopwords = remove_stopwords
        self.__preprocessor = self.__select_preprocessor(preprocessor_name=preprocessor_name)
        self.__tokinizer = Tokenizer(remove_stopwords=remove_stopwords)

    def preprocess_text(self, text: str) -> list:
        """
        Processes the input text by tokenizing it and then applying the selected preprocessing method (stemming or lemmatization).

        Parameters:
            text (str): The text to be preprocessed.

        Returns:
            list: A list of processed tokens from the input text.
        """
        tokens = self.__tokinizer.tokenize_and_filter_sentence(text)  # Tokenize and convert to lowercase
        return self.__preprocessor.preprocess_text(tokens)

    def __select_preprocessor(self, preprocessor_name) -> Stemmer | Lemmatizer:
        """
        Selects the appropriate preprocessor based on the provided name.

        Parameters:
            preprocessor_name (str): The name of the preprocessor.

        Returns:
            Stemmer | Lemmatizer: An instance of either Stemmer or Lemmatizer based on the specified preprocessor name.
        """
        if preprocessor_name == "Stemmer":
            return Stemmer()
        elif preprocessor_name == "Lemmatizer":
            return Lemmatizer()

    @property
    def preprocessor_name(self) -> str:
        """
        A property to get the name of the preprocessor being used.

        Returns:
            str: The name of the preprocessor.
        """
        return self.__preprocessor_name

    @property
    def remove_stopwords(self) -> bool:
        """
        A property to check if stopwords are being removed during tokenization.

        Returns:
            bool: True if stopwords are removed, False otherwise.
        """
        return self.__remove_stopwords

from tree_sitter import Language, Parser, Tree

from utilities.path_finder import PathFinder

AVAILABLE_LANGUAGE = ["python", "java", "c"]

OUTPUT_PATH = PathFinder().get_complet_path(path_to_file="ressources/tree-sitter/build/my-languages.so")

REPO_PATH = PathFinder().get_complet_path(path_to_file="ressources/tree-sitter/vendor/tree-sitter-")


class AbstractSyntaxTree:
    """
    A class for parsing source code into an abstract syntax tree (AST) using the tree_sitter library.

    Attributes:
        __parser (Parser): A tree_sitter Parser object used to parse source code.
        __languages (dict): A dictionary mapping language names to tree_sitter Language objects.

    Methods:
        parse(source_code, language): Parses the source code in the specified language into an AST.
    """

    def __init__(self):
        """
        Initializes the AbstractSyntaxTree class by setting up the tree-sitter library with required languages.
        """
        self.__initialize_library()
        self.__parser = Parser()
        self.__languages = {}
        for language in AVAILABLE_LANGUAGE:
            self.__languages[language] = Language(path_or_ptr=OUTPUT_PATH, name=language)

    def parse(self, source_code: str, language: str) -> Tree:
        """
        Parses the given source code into an abstract syntax tree.

        Parameters:
            source_code (str): The source code to parse.
            language (str): The programming language of the source code. Must be one of the supported languages.

        Returns:
            Tree: An abstract syntax tree of the parsed source code.
        """
        self.__parser.set_language(self.__languages[language])
        tree = self.__parser.parse(bytes(source_code, "utf-8"))
        return tree

    def __initialize_library(self) -> None:
        """
        Private method to build or load the tree-sitter language library required for parsing.
        """
        Language.build_library(
            # Store the library in the `build` directory
            OUTPUT_PATH,
            # Include one or more languages
            [REPO_PATH + language for language in AVAILABLE_LANGUAGE]
        )

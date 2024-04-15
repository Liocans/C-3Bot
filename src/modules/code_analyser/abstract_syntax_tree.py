from tree_sitter import Language, Parser, Tree

from utilities.path_finder import PathFinder

AVAILABLE_LANGUAGE = ["python", "java", "c"]

OUTPUT_PATH = PathFinder().get_complet_path(path_to_file="ressources/tree-sitter/build/my-languages.so")

REPO_PATH = PathFinder().get_complet_path(path_to_file="ressources/tree-sitter/vendor/tree-sitter-")


class AbstractSyntaxTree:
    def __init__(self):
        self.__initialize_library()
        self.__parser = Parser()
        self.__languages = {}
        for language in AVAILABLE_LANGUAGE:
            self.__languages[language] = Language(path_or_ptr=OUTPUT_PATH, name=language)

    def parse(self, source_code: str, language: str) -> Tree:
        self.__parser.set_language(self.__languages[language])
        tree = self.__parser.parse(bytes(source_code, "utf-8"))
        return tree

    def __initialize_library(self):
        Language.build_library(
            # Store the library in the `build` directory
            OUTPUT_PATH,
            # Include one or more languages
            [REPO_PATH + language for language in AVAILABLE_LANGUAGE]
        )

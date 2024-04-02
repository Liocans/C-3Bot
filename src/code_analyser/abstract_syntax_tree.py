from tree_sitter import Language, Parser

from utilities.file_searcher import PathFinder

AVAILABLE_LANGUAGE = ["python", "java", "c"]

OUTPUT_PATH = PathFinder().get_complet_path("ressources/tree-sitter/build/my-languages.so")

REPO_PATH = PathFinder().get_complet_path("ressources/tree-sitter/vendor/tree-sitter-")


class AbstractSyntaxTree:
    def __init__(self):
        self.__initialize_library()
        self.__parser = Parser()
        self.__languages = {}
        for language in AVAILABLE_LANGUAGE:
            self.__languages[language] = Language(OUTPUT_PATH, language)

    def parse(self, source_code, language):
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
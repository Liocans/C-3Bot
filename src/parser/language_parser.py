from tree_sitter import Language, Parser

from utilities.file_searcher import PathFinder

AVAILABLE_LANGUAGE = ["python", "java", "c"]

OUTPUT_PATH = PathFinder().get_complet_path("ressources/tree-sitter/build/my-languages.so")

REPO_PATH = PathFinder().get_complet_path("ressources/tree-sitter/vendor/tree-sitter-")


class LanguageParser:
    def __init__(self):
        self.__initialize_library()
        self.parser = Parser()
        self.languages = {}
        for language in AVAILABLE_LANGUAGE:
            self.languages[language] = Language(OUTPUT_PATH, language)

    def parse(self, source_code, language):
        self.parser.set_language(self.languages[language])
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        return tree

    def find_syntax_problem(self, source_code, language):
        errors = set()
        missings = set()
        tree = self.parse(source_code, language)
        todo = [tree.root_node]
        while todo:
            node = todo.pop()
            for child in node.children:
                if (child.type == "ERROR"):
                    errors.add((child.start_point[0] + 1, child.start_point[1] + 1))
                elif (child.is_missing):
                    missings.add((child.start_point[0] + 1, child.start_point[1] + 1, child.type))
                todo.append(child)

        return errors, missings

    def __initialize_library(self):
        Language.build_library(
            # Store the library in the `build` directory
            OUTPUT_PATH,
            # Include one or more languages
            [REPO_PATH + language for language in AVAILABLE_LANGUAGE]
        )
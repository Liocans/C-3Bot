from tree_sitter import Language, Parser

AVAILABLE_LANGUAGE = ["python","java","c"]

OUTPUT_PATH = "../ressources/tree-sitter/build/my-languages.so"

REPO_PATH = "../ressources/tree-sitter/vendor/tree-sitter-"

Language.build_library(
    # Store the library in the `build` directory
    OUTPUT_PATH,
    # Include one or more languages
    [REPO_PATH + language for language in AVAILABLE_LANGUAGE]
    )

class LanguageParser:
    def __init__(self):
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
                if(child.type == "ERROR"):
                    errors.add(child.start_point[0]+1)
                elif(child.is_missing):
                    missings.add((child.start_point[0]+1, child.type))
                todo.append(child)
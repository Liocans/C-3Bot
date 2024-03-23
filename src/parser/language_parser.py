from tree_sitter import Language, Parser
import tree_sitter_python as tspython
AVAILABLE_LANGUAGE = ["python","java","c"]

class LanguageParser:
    def __init__(self):
        self.parser = Parser()
        self.languages = {}
        for language in AVAILABLE_LANGUAGE:
            self.languages[language] = Language(tspython.language(), language)
        print(self.languages)

    def parse(self, source_code, language):
        self.parser.set_language(self.languages[language])
        tree = self.parser.parse(bytes(source_code, "utf-8"))
        return tree

    def find_errors(self,source_code,language):
        errors = set()
        tree = self.parse(source_code,language)
        todo = [tree.root_node]
        while todo:
            node = todo.pop()
            for child in node.children:
                if((child.is_missing or child.type == "ERROR")):
                    errors.add(child.start_point[0]+1)
                todo.append(child)
        print(errors)




if __name__ == '__main__':
    LanguageParser().find_errors("""de foo():
    if bar:
        baz()
""", "python")
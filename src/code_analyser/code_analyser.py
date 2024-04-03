from code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from code_analyser.clean_code_analyser import CleanCodeAnalyser
from code_analyser.syntax_analyser import SyntaxAnalyser


class CodeAnalyser:

    def __init__(self):
        self.syntax_tree = AbstractSyntaxTree()
        self.clean_analyser = CleanCodeAnalyser()
        self.syntax_analyser = SyntaxAnalyser()

    def analyse(self, text, language, mode="both"):
        descriptions = []
        tree = self.syntax_tree.parse(text, language)
        if (mode == "both" or mode == "S"):
            descriptions.extend(self.syntax_analyser.describe_problems(tree))

        if (mode == "both" or mode == "C"):
            descriptions.extend(self.clean_analyser.describe_clean_code_problems(tree))

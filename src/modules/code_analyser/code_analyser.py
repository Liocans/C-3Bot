from abstract_syntax_tree import AbstractSyntaxTree
from clean_code_analyser import describe_clean_code_problems
from syntax_analyser import describe_syntax_problems


class CodeAnalyser:

    def __init__(self):
        self.syntax_tree = AbstractSyntaxTree()

    def analyse(self, text, language, mode="both"):
        descriptions = []
        tree = self.syntax_tree.parse(text, language)
        if (mode == "both" or mode == "S"):
            descriptions.extend(describe_syntax_problems(tree))

        if (mode == "both" or mode == "C"):
            descriptions.extend(describe_clean_code_problems(tree))

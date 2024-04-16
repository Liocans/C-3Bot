from modules.code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from modules.code_analyser.clean_code_analyser import describe_clean_code_problems
from modules.code_analyser.syntax_analyser import find_syntax_problem

class CodeAnalyser:

    def __init__(self):
        self.syntax_tree = AbstractSyntaxTree()

    def analyse(self, code, language, mode="both"):
        descriptions = []
        if language in ["java","python","c"]:
            tree = self.syntax_tree.parse(code, language)
            if (mode == "both" or mode == "S"):
                descriptions.append(find_syntax_problem(tree, describe_problem=True))

            if (mode == "both" or mode == "C"):
                descriptions.append(describe_clean_code_problems(tree, language))
        else:
            descriptions.append("I'm really sorry but i don't know the language you gave me, i can only help you on "
                                "java, python or c")
        return descriptions

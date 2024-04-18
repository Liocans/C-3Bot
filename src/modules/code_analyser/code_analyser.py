from typing import List

from modules.code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from modules.code_analyser.clean_code_analyser import describe_clean_code_problems
from modules.code_analyser.syntax_analyser import find_syntax_problem


class CodeAnalyser:
    """
    A class for analyzing source code to identify syntax errors and clean code issues, based on specified programming languages.

    Attributes:
        syntax_tree (AbstractSyntaxTree): An instance of AbstractSyntaxTree used for parsing code into a syntax tree.

    Methods:
        analyse(code, language, mode): Analyzes the given code in the specified language and mode.
    """

    def __init__(self):
        self.syntax_tree = AbstractSyntaxTree()

    def analyse(self, code: str, language: str, mode: str = "both") -> str | list[str]:
        """
        Analyzes the given source code for syntax errors and clean code principles based on the specified language and mode.

        Parameters:
            code (str): The source code to analyze.
            language (str): The programming language of the source code. Currently supported languages are 'java', 'python', and 'c'.
            mode (str, optional): The mode of analysis to perform. Can be 'both' for both syntax and clean code analysis,
                                  'S' for only syntax analysis, or 'C' for only clean code analysis. Defaults to 'both'.

        Returns:
            list: A list containing results from the analysis. Each element can be a detailed description of problems found,
                  or a message indicating unrecognized language or other errors.
        """
        descriptions = []
        if language in ["java", "python", "c"]:
            tree = self.syntax_tree.parse(code, language)
            if (mode == "both" or mode == "S"):
                output = find_syntax_problem(tree, describe_problem=True)
                if (isinstance(output, str)):
                    descriptions.append(output)
                else:
                    descriptions.extend(output)

            if (mode == "both" or mode == "C"):
                output = describe_clean_code_problems(tree, language)
                if (isinstance(output, str)):
                    descriptions.append(output)
                else:
                    descriptions.extend(output)

        else:
            return ("I'm really sorry but i don't know the language you gave me, i can only help you on java, "
                    "python or c")
        return descriptions

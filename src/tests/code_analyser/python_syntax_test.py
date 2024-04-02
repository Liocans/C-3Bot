import unittest

from code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from code_analyser.syntax_analyser import SyntaxAnalyser
from utilities.file_searcher import PathFinder


class TestPythonParser(unittest.TestCase):

    def setUp(self):
        self.language_parser = AbstractSyntaxTree()

    def test_missings(self):
        filename = PathFinder().get_complet_path('ressources/python_files/code_with_missings.txt')
        expected_output = (set(), {(2, 50, ')')})
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(file.read(), "python")
            actual_output = SyntaxAnalyser.find_syntax_problem(syntax_tree)
        self.assertEqual(expected_output , actual_output)

    def test_errors(self):
        filename = PathFinder().get_complet_path('ressources/python_files/code_with_errors.txt')
        expected_output = ({(11, 20), (7, 1), (1, 1), (19, 35), (11, 31), (2, 5)}, {(2, 50, ')')})
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(file.read(), "python")
            actual_output = SyntaxAnalyser.find_syntax_problem(syntax_tree)
        self.assertEqual(expected_output, actual_output)

    def test_no_errors(self):
        filename = PathFinder().get_complet_path('ressources/python_files/code_without_errors.txt')
        expected_output = (set(), set())
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(file.read(), "python")
            actual_output = SyntaxAnalyser.find_syntax_problem(syntax_tree)
        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()

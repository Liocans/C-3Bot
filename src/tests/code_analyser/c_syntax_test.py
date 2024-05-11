import unittest

from modules.code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from modules.code_analyser.syntax_analyser import find_syntax_problem
from utilities.path_finder import PathFinder


class TestCParser(unittest.TestCase):

    def setUp(self):
        self.language_parser = AbstractSyntaxTree()
        self.language = "c"

    def test_missings(self):
        filename = PathFinder().get_complet_path(
            path_to_file=f'ressources/{self.language}_files/code_with_missings.txt')
        expected_output = ([8, 9, 10, 14, 15, 16, 18, 19, 20, 21, 22, 24], [(10, '"'), (25, ';')])
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = find_syntax_problem(syntax_tree=syntax_tree)
        self.assertEqual(actual_output, expected_output)

    def test_errors(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_with_errors.txt')
        expected_output = ([10, 11], [(10, '"')])
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = find_syntax_problem(syntax_tree=syntax_tree)
        self.assertEqual(actual_output, expected_output)

    def test_no_errors(self):
        filename = PathFinder().get_complet_path(
            path_to_file=f'ressources/{self.language}_files/code_without_errors.txt')
        expected_output = ([], [])
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = find_syntax_problem(syntax_tree=syntax_tree)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()

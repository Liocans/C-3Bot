import unittest

from modules.code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from modules.code_analyser.syntax_analyser import find_syntax_problem
from utilities.path_finder import PathFinder


class TestJavaParser(unittest.TestCase):

    def setUp(self):
        self.language_parser = AbstractSyntaxTree()
        self.language = "java"

    def test_missings(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_with_missings.txt')
        expected_output = ({(3, 1), (11, 25), (14, 28)}, {(5, 20, ';')})
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = find_syntax_problem(syntax_tree=syntax_tree)
        self.assertEqual(expected_output , actual_output)

    def test_errors(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_with_errors.txt')
        expected_output = (set(), {(37, 2, '}')})
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = find_syntax_problem(syntax_tree=syntax_tree)
        self.assertEqual(actual_output, expected_output)

    def test_no_errors(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_without_errors.txt')
        expected_output = (set(), set())
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = find_syntax_problem(syntax_tree=syntax_tree)
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()

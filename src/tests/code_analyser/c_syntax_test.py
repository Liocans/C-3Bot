import unittest

from modules.code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from modules.code_analyser.syntax_analyser import find_syntax_problem
from utilities.path_finder import PathFinder


class TestCParser(unittest.TestCase):

    def setUp(self):
        self.language_parser = AbstractSyntaxTree()
        self.language = "c"

    def test_missings(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_with_missings.txt')
        expected_output = (
            {(21, 28), (18, 38), (22, 26), (15, 11), (21, 12), (21, 30), (8, 5), (19, 11), (10, 11), (9, 31), (18, 12),
             (20, 12), (14, 11), (22, 12), (18, 36), (22, 24), (9, 12), (24, 12), (10, 25), (9, 33), (16, 11)},
            {(10, 28, '"'), (25, 2, ';')})
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = find_syntax_problem(syntax_tree=syntax_tree)
        self.assertEqual(actual_output, expected_output)

    def test_errors(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_with_errors.txt')
        expected_output = ({(11, 19), (10, 11)}, {(10, 27, '"')})
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

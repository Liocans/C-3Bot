import unittest

from code_analyser.abstract_syntax_tree import AbstractSyntaxTree
from code_analyser.clean_code_analyser import CleanCodeAnalyser
from utilities.file_searcher import PathFinder


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.language_parser = AbstractSyntaxTree()
        self.language = "c"

    def test_missings(self):
        filename = PathFinder().get_complet_path(path_to_file=f'ressources/{self.language}_files/code_with_cc.txt')
        expected_output = ()
        with open(filename, "r") as file:
            syntax_tree = self.language_parser.parse(source_code=file.read(), language=self.language)
            actual_output = CleanCodeAnalyser.describe_clean_code_problems(syntax_tree=syntax_tree, language=self.language)
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()

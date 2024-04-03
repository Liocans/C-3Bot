from tree_sitter import Tree


class SyntaxAnalyser:

    @staticmethod
    def find_syntax_problem(syntax_tree: Tree):
        errors = set()
        missings = set()
        todo = [syntax_tree.root_node]
        while todo:
            node = todo.pop()
            for child in node.children:
                if (child.type == "ERROR"):
                    errors.add((child.start_point[0] + 1, child.start_point[1] + 1))
                elif (child.is_missing):
                    missings.add((child.start_point[0] + 1, child.start_point[1] + 1, child.type))
                todo.append(child)

        return errors, missings

    @staticmethod
    def describe_problems(syntax_tree: Tree) -> str|list:
        errors, missings = SyntaxAnalyser.find_syntax_problem(syntax_tree=syntax_tree)
        descriptions = []

        for error in sorted(errors):
            line, char = error
            descriptions.append(f"There is an error at line {line} near character number {char}.")

        for missing in sorted(missings):
            line, char, missing_type = missing
            descriptions.append(f"There is a {missing_type} missing at line {line} near character number {char}.")

        if not descriptions:
            return "No syntax errors or missing elements found."

        return descriptions

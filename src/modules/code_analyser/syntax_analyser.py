from tree_sitter import Tree


def find_syntax_problem(syntax_tree: Tree, describe_problem: bool = False) -> tuple | list | str:
    """
    Scans a syntax tree for syntax errors or missing tokens and optionally provides a description of each problem.

    Parameters:
        syntax_tree (Tree): A tree_sitter Tree object representing the syntax tree of the source code.
        describe_problem (bool, optional): If True, returns a descriptive list of all syntax problems.
                                           If False, returns sets of errors and missing tokens. Defaults to False.

    Returns:
        tuple | list | str: Depending on the value of describe_problem:
            - If describe_problem is False, returns a tuple containing two sets: the first with the line and
              character numbers of errors, and the second with the line, character numbers, and types of missing tokens.
            - If describe_problem is True and issues are found, returns a list with a message and a set of descriptions.
            - If describe_problem is True and no issues are found, returns a string stating no syntax errors were detected.
    """
    errors = set()
    missings = set()
    descriptions = set()
    todo = [syntax_tree.root_node]

    while todo:
        node = todo.pop(0)
        for child in node.children:
            if (child.type == "ERROR"):
                if (describe_problem):
                    descriptions.add(
                        f"There is an error at line {child.start_point[0] + 1} near character number {child.start_point[1] + 1}.")
                errors.add((child.start_point[0] + 1, child.start_point[1] + 1))
            elif (child.is_missing):
                if (describe_problem):
                    descriptions.add(
                        f"There is a {child.type} missing at line {child.start_point[0] + 1} near character number {child.start_point[1] + 1}.")
                missings.add((child.start_point[0] + 1, child.start_point[1] + 1, child.type))
            todo.append(child)
    if describe_problem:
        if descriptions == set():
            return "I didn't detect syntax errors in your code"
        else:
            return ["Here is all the syntax problem i detected", list(descriptions)]
    return errors, missings

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
            - If describe_problem is False, returns a tuple containing two sorted lists: the first with the line and
              character numbers of errors, and the second with the line, character numbers, and types of missing tokens.
            - If describe_problem is True and issues are found, returns a list with a message and a sorted list of descriptions.
            - If describe_problem is True and no issues are found, returns a string stating no syntax errors were detected.
    """

    errors = set()
    missings = set()
    descriptions = set()
    todo = [syntax_tree.root_node]

    while todo:
        node = todo.pop(0)
        for child in node.children:
            if child.type == "ERROR":
                if describe_problem:
                    descriptions.add((child.start_point[0] + 1, f"There is an error at line {child.start_point[0] + 1}."))
                else:
                    errors.add(child.start_point[0] + 1)
            elif child.is_missing:
                if describe_problem:
                    descriptions.add((child.start_point[0] + 1, f"There is a {child.type} missing at line {child.start_point[0] + 1}."))
                else:
                    missings.add((child.start_point[0] + 1, child.type))
            todo.append(child)

    if describe_problem:
        if not descriptions:
            return "I didn't detect syntax errors in your code."
        else:
            # Sort descriptions by line number (the first element of each tuple)
            sorted_descriptions = sorted(descriptions, key=lambda x: x[0])
            # Extract only the second element of each tuple, which is the description
            description_messages = [desc[1] for desc in sorted_descriptions]
            return ["Here are all the syntax problems I detected:", description_messages]

    # Sort the errors and missing tokens based on the line number (first element of each tuple)
    sorted_errors = sorted(errors)
    sorted_missings = sorted(missings, key=lambda x: x[0])

    return sorted_errors, sorted_missings
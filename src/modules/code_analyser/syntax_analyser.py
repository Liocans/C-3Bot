from tree_sitter import Tree

def find_syntax_problem(syntax_tree: Tree, describe_problem=False):
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
            return ["Here is all the syntax problem i detected", descriptions]
    return errors, missings

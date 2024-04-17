import re

from tree_sitter import Tree, Node


def describe_clean_code_problems(syntax_tree: Tree, language: str) -> list | str:
    descriptions = set()
    todo = [syntax_tree.root_node]
    while todo:
        node = todo.pop(0)
        for child in node.named_children:

            if (child.type == "function_declarator"):
                new_descriptions = [
                    __function_namming_convention(node=child.child_by_field_name("declarator"),
                                                  language=language),
                    __function_length(node=child.parent),
                    __function_parameter_count(node=child.child_by_field_name("parameters"))]
                for new_description in new_descriptions:
                    if new_description != "":
                        descriptions.add(new_description)

            if (child.type in ["identifier", "field_identifier"]):
                if (child.parent.type not in ["call_expression", "function_declarator", "field_expression",
                                              "argument_list"]):
                    new_descriptions = [
                        __variable_namming_convention(node=child, language=language),
                        __namming_length(node=child)]
                    for new_description in new_descriptions:
                        if new_description != "":
                            descriptions.add(new_description)

            if (child.type == "class_declaration"):
                new_descriptions = [__class_namming_convention(node=child.child_by_field_name("name")),
                                    __namming_length(node=child.child_by_field_name("name"))]
                for new_description in new_descriptions:
                    if new_description != "":
                        descriptions.add(new_description)

            if (child.type == "struct_specifier"):
                new_descriptions = [
                    __struct_namming_convention(node=child.child_by_field_name("name")),
                    __namming_length(node=child.child_by_field_name("name"))]
                for new_description in new_descriptions:
                    if new_description != "":
                        descriptions.add(new_description)
            todo.append(child)

    if descriptions == set():
        return "I have not recommendation to do for the clean code"
    return ["Here is all the recommendation for the clean code", list(descriptions)]


# check if the name is too short to be understandable bigger or equal of 3
def __namming_length(node: Node) -> str:
    identifier = node.text.decode('utf-8')  # Assuming node.text contains the identifier's name
    if len(identifier) < 3:
        return f'Name too short at line {node.start_point[0] + 1} it should be should be at least 3 characters.'
    return ""


def __variable_namming_convention(node: Node, language: str) -> str:
    pattern = ""
    convention_pattern = ""
    identifier = node.text.decode('utf-8')
    if language == 'Python' or language == 'C':
        # Python & C: lowercase with underscores
        pattern = r'^[a-z_][a-z0-9_]*$'
        convention_pattern = "snake_case"
    elif language == 'Java':
        # Java: lowerCamelCase
        pattern = r'^[a-z][a-zA-Z0-9]*$'
        convention_pattern = "lowerCamelCase"
    return "" if re.match(pattern,
                          identifier) else f'Variable namming convention not respected at the line {node.start_point[0] + 1} it should be {convention_pattern}'


def __class_namming_convention(node: Node) -> str:
    identifier = node.text.decode('utf-8')

    return "" if re.match(r'^[A-Z][a-zA-Z0-9]*$',
                          identifier) else f'class namming convention not respected at the line {node.start_point[0] + 1} it should be UpperCamelCase'


def __struct_namming_convention(node: Node) -> str:
    identifier = node.text.decode('utf-8')

    return "" if re.match(r'^[A-Z][a-zA-Z0-9]*$',
                          identifier) else f'struct namming convention not respected at the line {node.start_point[0] + 1} it should be UpperCamelCase'


def __function_namming_convention(node: Node, language: str) -> str:
    pattern = ""
    pattern_name = ""
    identifier = node.text.decode('utf-8')
    if language == 'Python' or language == 'C':
        # Python & C: lowercase with underscores
        pattern = r'^[a-z_][a-z0-9_]*$'
        pattern_name = "snake_case"
    elif language == 'Java':
        # Java: lowerCamelCase
        pattern = r'^[a-z][a-zA-Z0-9]*$'
        pattern_name = "lowerCamelCase"

    return "" if re.match(pattern,
                          identifier) else f'Function namming convention not respected at the line {node.start_point[0] + 1} it should be {pattern_name}'


def __function_length(node: Node) -> str:
    # Assuming 'node' is a function node and it has a way to calculate its line span
    start_line = node.start_point[0]  # Assuming this gives the starting line number
    end_line = node.end_point[0]  # Assuming this gives the ending line number
    line_count = end_line - start_line
    if line_count > 20:
        return f"Function too long from line {start_line + 1} at line {end_line + 1}, try to keep the function length at 20 lines"
    return ""


def __function_parameter_count(node: Node) -> str:
    number_of_parameters = len(node.named_children)  # This will depend on your AST structure
    if number_of_parameters > 3:
        return f"Too many parameters for the function at line {node.start_point[0] + 1} try to only have 3 parameters if possible"
    return ""

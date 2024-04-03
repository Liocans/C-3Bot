import re

from tree_sitter import Node, Tree


class CleanCodeAnalyser:

    @staticmethod
    def describe_clean_code_problems(syntax_tree: Tree, language: str) -> list:
        descriptions = []
        todo = [syntax_tree.root_node]
        print(syntax_tree.root_node.children)
        while todo:
            node = todo.pop(0)
            for child in node.children:
                if (child.type == "function_declarator"):
                    description = CleanCodeAnalyser.__function_namming_convention(node=child.child_by_field_name("declarator"), language=language)
                    if description != "":
                        descriptions.append(description)
                    print(descriptions)
                if(child.type == "identifier"):
                    description = CleanCodeAnalyser.__namming_length(node=child)
                    if description != "":
                        descriptions.append(description)
                    print(descriptions)
                todo.append(child)


        return descriptions

    # This need to be different for each programming language
    @staticmethod
    def __function_namming_convention(node: Node, language: str) -> str:
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
                              identifier) else f'Function namming convention not respected at the line {node.start_point[0] + 1} it should be {convention_pattern}'

    @staticmethod
    def __variable_namming_convention(node: Node, language: str) -> str:
        print(node.text)
        return ""

    @staticmethod
    def __class_namming_convention(node: Node, language: str) -> str:
        identifier = node.text
        pattern = r'^[A-Z][a-zA-Z0-9]*$'
        convention_pattern = "UpperCamelCase"

        return "" if re.match(pattern,
                              identifier) else f'class namming convention not respected at the line {node.start_point[0] + 1} it should be {convention_pattern}'

    @staticmethod
    def __struct_namming_convention(node: Node, language: str) -> str:
        identifier = node.text
        pattern = r'^[A-Z][a-zA-Z0-9]*$'
        convention_pattern = "UpperCamelCase"

        return "" if re.match(pattern,
                              identifier) else f'struct namming convention not respected at the line {node.start_point[0] + 1} it should be {convention_pattern}'

    # check if the name is too short to be understandable bigger or equal of 3
    @staticmethod
    def __namming_length(node: Node) -> str:
        identifier = node.text.decode('utf-8')  # Assuming node.text contains the identifier's name
        print(identifier)
        if len(identifier) < 3:
            return f'Name too short at line {node.start_point[0] + 1} it should be should be at least 3 characters.'
        return ""

    # MAX 20 LINES
    @staticmethod
    def __function_length(node: Node) -> str:
        # Assuming 'node' is a function node and it has a way to calculate its line span
        start_line = node.start_point[0]  # Assuming this gives the starting line number
        end_line = node.end_point[0]  # Assuming this gives the ending line number
        line_count = end_line - start_line + 1
        if line_count > 20:
            return f"Function too long from line {start_line} to line {end_line}, try to keep the function length at 20 lines"
        return ""

    # MAX 3 arguments
    @staticmethod
    def __function_parameter_count(node: Node) -> str:
        parameters = node.parameters  # This will depend on your AST structure
        if len(parameters) > 3:
            return f"Too many parameters for the function line {node.start_point[0] + 1} try to only have 3 parameters if possible"
        return ""

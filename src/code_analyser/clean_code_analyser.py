from tree_sitter import Node, Tree


class CleanCodeAnalyser:

    @staticmethod
    def describe_clean_code_problems(syntax_tree: Tree) -> list:
        descriptions = []
        todo = [syntax_tree.root_node]
        while todo:
            node = todo.pop()
            for child in node.children:
                if ("identifier" in child.type):
                    descriptions.append(CleanCodeAnalyser.__namming_convention(child))
                    descriptions.append(CleanCodeAnalyser.__namming_length(child))
                todo.append(child)

        return descriptions

    #This need to be different for each programming language
    @staticmethod
    def __namming_convention(node: Node) -> str:
        print(node.text)
        return ""

    #check if the name is too short to be understandable bigger or equal of 3
    @staticmethod
    def __namming_length(node: Node) -> str:
        pass

    #MAX 20 LINES
    @staticmethod
    def __function_length(node: Node) -> str:
        pass

    #MAX 3 arguments
    @staticmethod
    def __function_parameter_count(node: Node) -> str:
        pass

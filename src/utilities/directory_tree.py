from pathlib import Path

from utilities.path_finder import PathFinder

# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '


def tree(dir_path: Path, prefix: str=''):
    """
    Generate a visual tree structure for the contents of a directory, excluding certain directories.

    The function recursively traverses through the directory structure starting from `dir_path`,
    yielding each directory and file in a visual format with branches and nodes. It excludes
    directories specifically named 'ressources', '.venv', and '.idea' from recursion.

    Parameters:
        dir_path (Path): The directory path from which to start generating the tree.
        prefix (str, optional): A string prefix used to represent the tree structure visually.
                                This gets extended as the function recurses deeper into the directory structure.

    Yields:
        str: A line in the visual representation of the directory tree.

    Example:
        ```
        # Assuming the use within a script or interactive session:
        base_path = Path("/path/to/directory")
        for line in tree(base_path):
            print(line)
        ```
    """
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.name != "ressources" and path.name != ".venv" and path.name != ".idea":
            if path.is_dir(): # extend the prefix and recurse:
                extension = branch if pointer == tee else space
                # i.e. space because last, └── , above so no more |
                yield from tree(path, prefix=prefix+extension)

if __name__ == '__main__':
    for line in tree(Path(PathFinder.get_basic_path())):
        print(line)
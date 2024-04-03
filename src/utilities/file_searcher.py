import re
import os


class PathFinder:
    _path = None
    _pattern = r"^(.*\\src).*"

    @staticmethod
    def get_basic_path() -> str:
        if PathFinder._path == None:
            app_dir_os = os.path.dirname(os.path.abspath(__file__))
            PathFinder._path = re.sub(PathFinder._pattern, r"\1", app_dir_os)

        return PathFinder._path

    @staticmethod
    def get_complet_path(path_to_file: str) -> str:
        return PathFinder.get_basic_path() + "/" + path_to_file

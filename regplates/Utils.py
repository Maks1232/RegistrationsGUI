import os 
import regplates

def get_resource_path(*paths: str | os.PathLike) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(regplates.__file__)), 'Resources', *paths)
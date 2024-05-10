from __future__ import annotations

import os


def get_resource_path(*paths: str | os.PathLike) -> str:
    if __package__:
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)), __package__, *paths
        )
    else:
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "regplates", *paths
        )

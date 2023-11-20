from filesys import FileSys
import yaml
from typing import Dict, List, Union, Optional, Union, Callable, Any
from functools import lru_cache

CONFIG_PATH = "config.yml"


@lru_cache(maxsize=None)
def get_config(path: str = CONFIG_PATH) -> Dict:
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


def create_paths(config: Dict, root_path: str) -> None:
    fs = FileSys.init_from_path(path=root_path)
    download_structure = config["downloads"]
    fs.create_structure(download_structure)


create_paths(config=get_config(), root_path="./data")

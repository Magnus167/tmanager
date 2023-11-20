from typing import Dict, Union, Callable, Optional, List, Any
from pathlib import Path
import glob
from functools import lru_cache
import hashlib


def hash_object(obj: object) -> str:
    return hashlib.sha256(str(obj).encode("utf-8")).hexdigest()


def path_to_hash(path: Path) -> str:
    return hash_object(path)


def _get_glob(path: str, recursive=True, *args, **kwargs) -> List[str]:
    return glob.glob(path, recursive=recursive, *args, **kwargs)


def path_to_dict(path: Path) -> Dict[str, Union[str, Dict]]:
    path_glob = _get_glob(f"{str(path)}/*", recursive=True)
    structure = {}
    for item in path_glob:
        if Path(item).is_dir():
            structure[item] = path_to_dict(Path(item))
        else:
            structure[item] = ""
    return structure


def apply_func(
    path: Path,
    func: Callable[[Path], Any],
    *args,
    **kwargs,
) -> Optional[Any]:
    if path.exists():
        return func(path, *args, **kwargs)
    else:
        raise FileNotFoundError(f"Path {path} does not exist.")


def struct_apply(
    structure: Dict[str, Union[str, Dict]],
    root_path: Path,
    func: Callable[[Path], Any],
    *args,
    **kwargs,
) -> None:
    for name, content in structure.items():
        if isinstance(content, dict):
            struct_apply(structure=content, root_path=root_path / name, func=func)
        else:
            apply_func(path=root_path / name, func=func, *args, **kwargs)


def create_file(
    path: Path,
    content: Union[str, bytes],
    overwrite: bool = False,
    *args,
    **kwargs,
) -> None:
    if isinstance(content, str):
        content = content.encode("utf-8")
    try:
        if path.exists():
            if overwrite:
                path.unlink()
            else:
                raise FileExistsError(f"File {path} already exists.")
        path.write_bytes(content, *args, **kwargs)
    except Exception as exc:
        raise Exception(f"Error while creating file {path}") from exc


def create_directory(path: Path, exists_ok: bool = True, *args, **kwargs) -> None:
    # Revised to handle exists_ok properly
    try:
        path.mkdir(parents=True, exist_ok=exists_ok)
    except Exception as exc:
        raise Exception(f"Error while creating directory {path}") from exc


def create_structure(
    structure: Dict[str, Union[str, Dict]],
    root_path: Path,
    exists_ok: bool = None,
    overwrite: bool = None,
    *args,
    **kwargs,
) -> None:
    if isinstance(structure, list):
        struct_dict: Dict[str, Union[str, Dict]] = {}
        for item in structure:
            if not isinstance(item, dict):
                struct_dict[str(item)] = {}
            else:
                struct_dict.update(item)
        structure = struct_dict.copy()

    for name, content in structure.items():
        if isinstance(content, list):
            content_dict: Dict[str, Union[str, Dict]] = {}
            for item in content:
                if not isinstance(item, dict):
                    content_dict[str(item)] = {}
                else:
                    content_dict.update(item)
            content = content_dict.copy()

        if isinstance(content, dict):
            create_directory(path=root_path / name, exists_ok=exists_ok)
            create_structure(structure=content, root_path=root_path / name)
        else:
            create_file(path=root_path / name, content=content, overwrite=overwrite)


class FileSys:
    def __init__(
        self,
        structure: Dict[str, Union[str, Dict]],
        root_path: str = ".",
        exists_ok: bool = True,
        overwrite: bool = False,
        create_mode: bool = True,
    ) -> None:
        self.structure: Dict[str, Union[str, Dict]] = {}
        for name, content in structure.items():
            if isinstance(content, dict):
                self.structure[name] = content
            else:
                self.structure[name] = {}

        self.root_path: Path = Path(root_path)
        self.exists_ok: bool = exists_ok
        self.overwrite: bool = overwrite
        if create_mode:
            self.create_structure(self.structure, self.root_path)

    @classmethod
    def init_from_path(cls, path: str, exists_ok: bool = True, overwrite: bool = False):
        root_path = Path(path)
        structure = path_to_dict(path=root_path)
        return cls(
            structure=structure,
            root_path=root_path,
            exists_ok=exists_ok,
            overwrite=overwrite,
            create_mode=False,
        )

    def _update_structure(self) -> None:
        self.structure = path_to_dict(self.root_path)

    def get_structure(self) -> Dict[str, Union[str, Dict]]:
        self._update_structure()
        return self.structure

    def create_file(self, path: Path, content: str, overwrite: bool = None) -> None:
        if overwrite is None:
            overwrite = self.overwrite
        create_file(path, content, overwrite=overwrite)

    def create_structure(
        self,
        structure: Dict[str, Union[str, Dict]],
        root_path: Optional[Path] = None,
        exists_ok: bool = None,
        overwrite: bool = None,
        *args,
        **kwargs,
    ) -> None:
        create_structure(
            structure=structure,
            root_path=self.root_path if root_path is None else root_path,
            exists_ok=self.exists_ok if exists_ok is None else exists_ok,
            overwrite=self.overwrite if overwrite is None else overwrite,
            *args,
            **kwargs,
        )
        self._update_structure()

    def create_directory(self, path: Path, *args, **kwargs) -> None:
        create_directory(path=path, *args, **kwargs)
        self._update_structure()

    def apply(
        self,
        path: str,
        func: Callable[[Path], Any],
        *args,
        **kwargs,
    ) -> Optional[Any]:
        target_path = self.root_path / path
        return apply_func(target_path, func, *args, **kwargs)

    def struct_apply(
        self,
        func: Callable[[Path], Any],
        *args,
        **kwargs,
    ) -> None:
        struct_apply(
            structure=self.structure,
            root_path=self.root_path,
            func=func,
            *args,
            **kwargs,
        )

    def get(self, path: str) -> Optional[Path]:
        target_path = self.root_path / path
        if target_path.exists():
            return target_path
        else:
            print(f"Path {path} does not exist.")
            return None

    def search(self, pattern: str) -> List[Path]:
        self._update_structure()
        return list(self.root_path.glob(pattern))


# # Example usage
# structure = {
#     "Folder1": {
#         "Subfolder1": {
#             "file1.txt": "Content of file1",
#             "file2.txt": "Content of file2",
#         },
#         "Subfolder2": {
#             "file3.txt": "Content of file3",
#         },
#     },
#     "Folder2": {
#         "file4.txt": "Content of file4",
#     },
# }

# fs = FileSys(structure, root_path="my_directory")

# # Example of search method
# results = fs.search("**/*.txt")
# for path in results:
#     print(path)

# # Example usage
# fs_from_path = FileSys.init_from_path(
#     path="path_to_existing_directory",
#     exists_ok=True,
#     overwrite=False,
# )

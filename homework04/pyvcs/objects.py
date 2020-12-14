import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    hash_name = hashlib.sha1(store).hexdigest()

    if write:
        path = repo_find() / "objects" / hash_name[:2]

        if os.path.exists(path / hash_name[2:]):
            return hash_name

        os.mkdir(path)
        with open(path / hash_name[2:], "wb") as f:
            f.write(zlib.compress(store))

    return hash_name


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) < 4 or len(obj_name) > 40:
        raise Exception(f"Not a valid object name {obj_name}")

    result = []
    path = repo_find(gitdir) / "objects" / obj_name[:2]
    for root, dir, files in os.walk(path):
        for filename in files:
            if filename.startswith(obj_name[2:]):
                result.append(obj_name[:2] + filename)
            else:
                raise Exception(f"Not a valid object name {obj_name}")
    return result


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = repo_find(gitdir) / "objects" / sha[:2]
    with open(path / sha[2:], mode="rb") as f:
        obj_data = zlib.decompress(f.read())

    header = obj_data[: obj_data.find(b"\x00")]
    header_index = header.find(b" ")
    header = header[:header_index]
    content = obj_data[obj_data.find(b"\x00") + 1 :]
    return header.decode(), content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result = []
    while len(data) != 0:
        mode = int(data[: data.find(b" ")].decode())
        data = data[data.find(b" ") + 1 :]
        name = data[: data.find(b"\x00")].decode()
        data = data[data.find(b"\x00") + 1 :]
        sha = bytes.hex(data[:20])
        data = data[20:]
        result.append((mode, name, sha))
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = repo_find(".")
    if len(resolve_object(obj_name, gitdir)) != 0:
        header, content = read_object(obj_name, gitdir)
        if header == "tree":
            result = ""
            tree_files = read_tree(content)
            for file in tree_files:
                result += str(file[0]).zfill(6) + " "
                result += read_object(file[2], repo_find())[0] + " "
                result += file[2] + "\t"
                result += file[1] + "\n"
            print(result)
        else:
            print(content.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    header, data = read_object(tree_sha, gitdir)
    for file in read_tree(data):
        if read_object(file[2], gitdir)[0] == "tree":
            tree = find_tree_files(file[2], gitdir)
            for blob in tree:
                name = file[1] + "/" + blob[0]
            result.append((name, blob[1]))
        else:
            result.append((file[1], file[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    return data[data.find(b"tree") + 5 : data.find(b"tree") + 45]

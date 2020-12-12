import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths, True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    index = read_index(gitdir)
    tree_sha = write_tree(gitdir, index)
    return commit_tree(gitdir, tree=tree_sha, message=message, author=author)


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    if is_detached(gitdir) and get_ref(gitdir) == obj_name:
        return
    elif get_ref(gitdir).split("/")[2] == obj_name:
        return
    elif resolve_head(gitdir) == obj_name:
        return
    elif (gitdir / "refs" / "heads" / obj_name).exists():
        with open(gitdir / "refs" / "heads" / obj_name, "r") as f1:
            obj_name = f1.read()

    index = read_index(gitdir)
    for entry in index:
        if os.path.exists(entry.name):
            if "/" in entry.name:
                shutil.rmtree(entry.name[: entry.name.find("/")])
            else:
                os.remove(entry.name)

    with open(gitdir / "objects" / obj_name[:2] / obj_name[2:], "rb") as f2:
        commit_content = f2.read()
    tree_sha = commit_parse(commit_content).decode()

    for file in find_tree_files(tree_sha, gitdir):
        if "/" in file[0]:
            dir_name = file[0][: file[0].find("/")]
            os.mkdir(dir_name)
        with open(file[0], "w") as f3:
            header, content = read_object(file[1], gitdir)
            f3.write(content.decode())

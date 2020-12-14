import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    records = b""
    for entry in index:
        if "/" in entry.name:
            records += b"40000 "
            subdir_files = b""
            dir_name = entry.name[: entry.name.find("/")]
            records += dir_name.encode() + b"\0"
            subdir_files += oct(entry.mode)[2:].encode() + b" "
            subdir_files += entry.name[entry.name.find("/") + 1 :].encode() + b"\0"
            subdir_files += entry.sha1
            blob_hash = hash_object(subdir_files, fmt="tree", write=True)
            records += bytes.fromhex(blob_hash)
        else:
            records += oct(entry.mode)[2:].encode() + b" "
            records += entry.name.encode() + b"\0"
            records += entry.sha1
    tree_name = hash_object(records, fmt="tree", write=True)
    return tree_name


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    seconds_time = str(int(time.mktime(time.localtime()))).encode()
    timezone = "{:+}00".format(int(time.timezone / -3600)).zfill(5).encode()
    if author is None:
        author = "{} <{}>".format(os.getenv("GIT_AUTHOR_NAME"), os.getenv("GIT_AUTHOR_EMAIL"))
    assert isinstance(author, str)
    if parent:
        assert isinstance(parent, str)
        result = b"tree %s\nparent %s\nauthor %s %s %s\ncommitter %s %s %s\n\n%s\n" % (
            tree.encode(),
            parent.encode(),
            author.encode(),
            seconds_time,
            timezone,
            author.encode(),
            seconds_time,
            timezone,
            message.encode(),
        )
    else:
        result = b"tree %s\nauthor %s %s %s\ncommitter %s %s %s\n\n%s\n" % (
            tree.encode(),
            author.encode(),
            seconds_time,
            timezone,
            author.encode(),
            seconds_time,
            timezone,
            message.encode(),
        )
    return hash_object(result, fmt="commit", write=True)

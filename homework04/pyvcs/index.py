import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        name_length = len(self.name)
        values = (
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            self.name.encode(),
        )
        packed = struct.pack(
            "!LLLLLLLLLL20sH%ds%dx" % (name_length, 8 - ((62 + name_length) % 8)), *values
        )
        return packed

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        name_length = len(data[62:])
        head = struct.unpack("!LLLLLLLLLL20sH", data[:62])
        name = struct.unpack("!%ss" % name_length, data[62:])[0]
        name = name.strip(b"\x00").decode()
        return GitIndexEntry(*(head + (name,)))


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    result = []
    if os.path.exists(gitdir / "index"):
        with open(gitdir / "index", "rb") as f:
            data = f.read()
        entry_count = struct.unpack("!L", data[8:12])[0]
        start_pos = 12
        for i in range(entry_count):
            end_pos = start_pos + 62 + data[start_pos + 62 :].find(b"\x00")
            entry = data[start_pos:end_pos]
            result.append(GitIndexEntry.unpack(entry))
            start_pos = end_pos + (8 - ((62 + len(result[i].name)) % 8))
    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    result = struct.pack("!4sLL", b"DIRC", 2, len(entries))
    for entry in entries:
        result += entry.pack()
    result += bytes.fromhex(hashlib.sha1(result).hexdigest())
    with open(gitdir / "index", "wb") as f:
        f.write(result)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    if details:
        indexes = read_index(gitdir)
        result = []
        string = ""
        for index in indexes:
            string += str(oct(index.mode)[2:]) + " "
            string += str(bytes.hex(index.sha1)) + " "
            string += "0\t"
            string += index.name
            result.append(string)
            string = ""
        print("\n".join(result))
    else:
        file_names = [index.name for index in read_index(gitdir)]
        print("\n".join(file_names))


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    entries = []
    for path in paths:
        with open(path, "r") as f:
            content = f.read()
        sha1 = hash_object(content.encode(), "blob", write=True)
        file = os.stat(path)
        entries.append(
            GitIndexEntry(
                ctime_s=round(file.st_ctime),
                ctime_n=0,
                mtime_s=round(file.st_mtime),
                mtime_n=0,
                dev=file.st_dev,
                ino=file.st_ino,
                mode=file.st_mode,
                uid=file.st_uid,
                gid=file.st_gid,
                size=file.st_size,
                sha1=bytes.fromhex(sha1),
                flags=len(path.name),
                name=str(path),
            )
        )

    if not (gitdir / "index").exists():
        write_index(gitdir, entries)
    else:
        index = read_index(gitdir)
        index += entries
        write_index(gitdir, index)

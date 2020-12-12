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
        name_length = len(self.name) + 3
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
        packed = struct.pack("!LLLLLLLLLL20sH%ds" % name_length, *values)
        return packed

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        name_length = len(data[62:])
        (
            ctime_s,
            ctime_n,
            mtime_s,
            mtime_n,
            dev,
            ino,
            mode,
            uid,
            gid,
            size,
            sha1,
            flags,
            name,
        ) = struct.unpack("!LLLLLLLLLL20sH%ds" % name_length, data)
        name = name.decode().replace("\x00", "")
        return GitIndexEntry(
            ctime_s=ctime_s,
            ctime_n=ctime_n,
            mtime_s=mtime_s,
            mtime_n=mtime_n,
            dev=dev,
            ino=ino,
            mode=mode,
            uid=uid,
            gid=gid,
            size=size,
            sha1=sha1,
            flags=flags,
            name=name,
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    result = []
    if os.path.exists(gitdir / "index"):
        with open(gitdir / "index", "rb") as f:
            data = f.read()
        index_entries = data[12:-20]
        sizes = [
            i + 7
            for i in range(len(index_entries))
            if index_entries.startswith(b".txt\x00\x00\x00", i)
        ]
        sizes.insert(0, 0)
        for i in range(len(sizes) - 1):
            result.append(GitIndexEntry.unpack(index_entries[sizes[i] : sizes[i + 1]]))
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

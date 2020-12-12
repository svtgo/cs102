import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    if workdir == ".":
        workdir = pathlib.Path(".")
    if isinstance(workdir, str):
        workdir = pathlib.Path(workdir)

    if ".git" in os.listdir(workdir):
        return workdir / ".git"
    elif workdir.parent.name == ".git":
        return workdir.parent
    elif workdir.name == ".git":
        return workdir
    else:
        raise Exception("Not a git repository")


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    if not os.getenv("GIT_DIR"):
        os.environ["GIT_DIR"] = ".git"
    dir_name = os.environ["GIT_DIR"]

    if isinstance(workdir, str):
        path = pathlib.Path(workdir) / dir_name
    else:
        path = workdir / dir_name

    try:
        os.mkdir(path)
    except OSError:
        assert isinstance(workdir, pathlib.PosixPath)
        raise Exception(f"{workdir.name} is not a directory")

    os.mkdir(path / "refs")
    os.mkdir(path / "refs" / "heads")
    os.mkdir(path / "refs" / "tags")
    os.mkdir(path / "objects")

    with open(path / "HEAD", "w+") as f:
        f.write("ref: refs/heads/master\n")

    with open(path / "config", "w+") as f:
        f.write(
            "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
        )

    with open(path / "description", "w+") as f:
        f.write("Unnamed pyvcs repository.\n")

    return path

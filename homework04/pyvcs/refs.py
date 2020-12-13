import pathlib
import typing as tp


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    if isinstance(ref, str):
        ref = pathlib.Path(ref)

    path = gitdir / ref
    path.touch()
    path.write_text(new_value)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with (gitdir / "HEAD").open("w") as f:
        f.write(name)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> tp.Union[str, None]:
    if refname == "HEAD":
        with open(gitdir / refname, "r") as f:
            content = f.read()
        refname = content[content.find(" ") + 1 :].strip()

    path = gitdir / refname
    if path.exists() is False:
        return None
    with open(path, "r") as f:
        content = f.read()

    return content


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    if ref_resolve(gitdir, "HEAD") is None:
        return None
    else:
        return ref_resolve(gitdir, "HEAD")


def is_detached(gitdir: pathlib.Path) -> bool:
    path = gitdir / "HEAD"

    with open(path, "r") as f:
        content = f.read()

    if content.startswith("ref:"):
        return False
    else:
        return True


def get_ref(gitdir: pathlib.Path) -> str:
    with open(gitdir / "HEAD", "r") as f:
        content = f.read()
    if is_detached(gitdir):
        return content
    else:
        refname = content[content.find(" ") + 1 :].strip()
        return refname

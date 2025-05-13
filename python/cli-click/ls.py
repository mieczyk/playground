from pathlib import Path
import click


def __print_dir_content(dir: Path) -> None:
    for item in dir.iterdir():
        padding = len(item.name) + 5
        # Make sure there's space between entries and no new line is printed (nl=False).
        click.echo(f"{item.name:{padding}}", nl=False)
    click.echo()


@click.command()
@click.argument("path", default=".")
def ls(path: str) -> None:
    """List directories and files in PATH.

    If no PATH given, the default dir is '.'
    """
    target_dir = Path(path)

    if not target_dir.exists():
        click.echo(f"Directory {path} does not exist!")
        raise SystemExit(1)

    __print_dir_content(target_dir)


@click.command()
@click.argument(
    # `click.Path`` is similar to `click.File` but it returns file path instead of an open file.
    # `exists=True` -> the file/dir must exist for the argument to be valid.
    # `file_okay=False` -> only directories are allowed.
    # `readable=True` -> valid if a user can read the directoriy's content (has sufficient permissions).
    # `path_type=Path` -> argument passed to the command is the `Path` type.
    "path",
    type=click.Path(exists=True, file_okay=False, readable=True, path_type=Path),
    default=Path("."),
)
def ls_with_path_type(path: Path) -> None:
    """List directories and files in PATH.

    If no PATH given, the default dir is '.'
    """

    # The `click.Path` argument type handles the path validation, so at this point
    # we're sure that the argument is valid.
    __print_dir_content(path)


if __name__ == "__main__":
    # ls()
    ls_with_path_type()

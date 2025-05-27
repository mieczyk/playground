from io import TextIOWrapper
from typing import Tuple

import click


@click.command()
# nargs=-1 <- undetermined number of input parameters.
# With the `click.File` input type, the files are already open
# and automatically closed after the command finished working.
@click.argument("files", type=click.File(mode="r"), nargs=-1)
def cat(files: Tuple[TextIOWrapper]) -> None:
    """Shows content of given FILE(S).
    """
    for file in files:
        click.echo(f"===== {file.name} ==== \n")
        click.echo(file.read().rstrip())


if __name__ == "__main__":
    cat()

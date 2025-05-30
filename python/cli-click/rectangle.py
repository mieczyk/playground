from typing import Tuple

import click


def print_size(size: Tuple[int, int]) -> None:
    width, height = size
    click.echo(f"Rectangle size: {width}x{height}")


@click.command()
# Accepts exactly 2 options (no more, no less)
@click.option(
    "-s",
    "--size",
    required=True,
    type=click.INT,
    nargs=2,
    help="Rectangle size in the following format: width height",
)
def rectangle_with_size_nargs(size: Tuple[int, int]) -> None:
    """Prints given size of a rectangle."""
    print_size(size)


@click.command()
# Accepts exactly 2 options (no more, no less).
# Uses standard tuple type to enforce validation.
@click.option(
    "-s",
    "--size",
    required=True,
    type=(click.INT, click.INT),
    help="Rectangle size in the following format: width height",
)
def rectangle_with_size_tuple_type(size: Tuple[int, int]) -> None:
    """Prints given size of a rectangle."""
    print_size(size)


if __name__ == "__main__":
    # rectangle_with_size_nargs()
    rectangle_with_size_tuple_type()

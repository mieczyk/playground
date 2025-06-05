# `deque` is a double-ended queue that supports both FIFO and LIFO operations.
# In other words: you can add/remove elements to/from both ends of the queue.
from collections import deque
from io import TextIOWrapper

import click


@click.command()
@click.option(
    "-n",
    "--lines",
    type=click.INT,
    default=10,
    help="How many last lines is displayed (default:10)",
)
@click.argument("file", type=click.File(mode="r"))
def tail(file: TextIOWrapper, lines: int) -> None:
    """Shows last N lines of a given file. Default N = 10.
    Works similarly Unix's `tail` command.
    """

    # File-like objects are iterators that produce a line of text on each iteration.
    # That's why we can pass the TextIOWrapper object to the deque container.
    #
    # `maxlen` determines the maximus size of the container.
    # `deque([1,2,3], maxlen=2)` contains only two last elements: [2,3].
    for line in deque(file, maxlen=lines):
        click.echo(line, nl=False)


if __name__ == "__main__":
    tail()

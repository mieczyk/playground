from typing import Tuple

import click


@click.command()
@click.option(
    "-p",
    "--profile",
    required=True,
    type=click.Tuple([str, int]),
    help="Profile information: name age",
)
def person(profile: Tuple[str, int]) -> None:
    """Prints person's profile information (name and age)."""
    click.echo(f"Hello, {profile[0]}! You're {profile[1]} years old.")


if __name__ == "__main__":
    person()

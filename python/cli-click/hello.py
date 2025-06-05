import click


@click.command("hello")
@click.version_option(
    "0.1.0", prog_name="hello"
)  # Information displayed if `--version` option given.
def hello():
    click.echo("Hello, world!")


if __name__ == "__main__":
    hello()

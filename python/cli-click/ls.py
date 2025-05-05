from pathlib import Path
import click

@click.command()
@click.argument("path", default=".")
def cli(path: str) -> None:
    """List directories and files in PATH.

    If no PATH given, the default dir is '.'
    """
    target_dir = Path(path)
    
    if not target_dir.exists():
        click.echo(f"Directory {path} does not exist!")
        raise SystemExit(1)
    
    for item in target_dir.iterdir():
        padding = len(item.name) + 5
        # Make sure there's space between entries and no new line is printed (nl=False).
        click.echo(f"{item.name:{padding}}", nl=False)
    click.echo()

if __name__ == "__main__":
    cli()
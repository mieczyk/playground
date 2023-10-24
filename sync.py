# TODO: Automatically sync the local changes with the GitHub repository.

from git import Repo
from pathlib import Path

repo = Repo(Path(__file__).parent)
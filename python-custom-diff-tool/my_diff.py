import argparse
import difflib
import sys

from pathlib import Path

MAX_FILE_LINES = 10_000

def create_diff(file1_path: Path, file2_path: Path, result_file_path: Path = None) -> None:
    file1 = open(file1_path).readlines(MAX_FILE_LINES)
    file2 = open(file2_path).readlines(MAX_FILE_LINES)

    if result_file_path:
        # Export results to the given XML file.
        html_diff = difflib.HtmlDiff()
        delta = html_diff.make_file(file1, file2, file1_path.name, file2_path.name)

        with open(result_file_path, "w") as result_file:
            result_file.write(delta)
    else:
        # Display results in STDOUT.
        # It seems that it doesn't analyza the whole file if it's too large. Check in the docs!
        delta = difflib.unified_diff(file1, file2, file1_path.name, file2_path.name)
        sys.stdout.writelines(delta)


def main(args: argparse.Namespace) -> None:
    file1_path = Path(args.file1)
    file2_path = Path(args.file2)    
    result_file_path = Path(args.html) if args.html else None

    create_diff(file1_path, file2_path, result_file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("file1")
    parser.add_argument("file2")
    parser.add_argument("--html", help="Save results to a given HTML file.")
    
    main(parser.parse_args())

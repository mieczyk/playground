import argparse
import difflib
import logging
import sys

from pathlib import Path

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def create_diff(file1_path: Path, file2_path: Path, result_file_path: Path = None) -> None:
    # readlines(hint=-1) - `hint` is the number of maximum bytes/characters that can be read.
    # Values of 0 or less (and None) are treated as no limit.
    file1 = open(file1_path).readlines()
    logging.debug(f"Read {len(file1)} lines from file {file1_path}")

    file2 = open(file2_path).readlines()
    logging.debug(f"Read {len(file2)} lines from file {file2_path}")

    if result_file_path:
        # Export results to the given XML file.
        html_diff = difflib.HtmlDiff()
        delta = html_diff.make_file(file1, file2, file1_path.name, file2_path.name)

        with open(result_file_path, "w") as result_file:
            result_file.write(delta)
    else:
        # Send results to STDOUT.
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

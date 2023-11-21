import argparse

def main(args: argparse.Namespace):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("file1")
    parser.add_argument("file2")
    parser.add_argument("--html", help="Save results to a given HTML file.")
    
    main(parser.parse_args())

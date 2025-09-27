from argparse import ArgumentParser


class IOBound:
    def download_page(self):
        pass

    def download_page_async(self):
        pass


class CPUBound:
    def calculate_something(self):
        pass

    def calculate_something_async(self):
        pass


if __name__ == "__main__":
    parser = ArgumentParser(
        description="The script demonstrates that async/await approach works the best with the I/O-bound tasks."
    )
    parser.add_argument("task_type", choices=["cpu", "io"])
    parser.add_argument(
        "-a",
        "--async",
        action="store_true",
        dest="use_async",
        help="Run tasks asynchronously.",
    )
    parser.add_argument(
        "-s",
        "--sync",
        action="store_false",
        dest="use_async",
        help="Run tasks synchronously (default).",
    )
    args = parser.parse_args()

    print(args.task_type)
    print(args.use_async)

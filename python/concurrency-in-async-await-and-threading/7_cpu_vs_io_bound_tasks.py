from argparse import ArgumentParser
import asyncio
import httpx
import time
from enum import Enum
from utils import measure_execution_time


class TaskType(str, Enum):
    cpu = "cpu"
    io = "io"


class IOBound:
    # httpbin.org is an HTTP test server.
    TEST_URL = "https://vilya.pl/"
    COUNT = 10

    def download_pages(self) -> None:
        with httpx.Client() as client:
            for _ in range(self.COUNT):
                url = f"{self.TEST_URL}?t={time.time()}"
                response = client.get(url)
                print(f"[sync] GET {url}: {response.status_code}")

    async def download_pages_async(self) -> None:
        async with httpx.AsyncClient() as client:
            queue = []
            for _ in range(self.COUNT):
                url = f"{self.TEST_URL}?t={time.time()}"
                queue.append(self.__get_page_async(client, url))
            await asyncio.gather(*queue)

    async def __get_page_async(self, client: httpx.AsyncClient, url: str) -> None:
        response = await client.get(url)
        print(f"[async] GET {url}: {response.status_code}")


class CPUBound:
    def calculate_something(self):
        pass

    async def calculate_something_async(self):
        pass


def main(task_type: TaskType) -> None:
    print(f"Running synchronous {task_type}-bound task...")
    if task_type == TaskType.io:
        task = IOBound()
        task.download_pages()
    else:
        task = CPUBound()
        task.calculate_something()


async def main_async(task_type: TaskType) -> None:
    print(f"Running asynchronous {task_type}-bound task...")
    if task_type == TaskType.io:
        task = IOBound()
        await task.download_pages_async()
    else:
        task = CPUBound()
        await task.calculate_something_async()


if __name__ == "__main__":
    parser = ArgumentParser(
        description="The script demonstrates that async/await approach works the best with the I/O-bound tasks."
    )
    parser.add_argument("task_type", choices=[TaskType.cpu, TaskType.io])
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

    with measure_execution_time():
        if args.use_async:
            asyncio.run(main_async(args.task_type))
        else:
            main(args.task_type)

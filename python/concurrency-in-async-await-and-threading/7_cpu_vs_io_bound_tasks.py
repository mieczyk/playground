from argparse import ArgumentParser
import asyncio
from typing import List
import httpx
import time
import random
from enum import Enum
from utils import measure_execution_time


class TaskType(str, Enum):
    cpu = "cpu"
    io = "io"


class IOBound:
    TEST_URL = "https://github.com"
    COUNT = 20

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
    TEST_IMG_SIZE = (1960, 1080)
    COUNT = 2

    def __init__(self):
        random.seed(42)

    def generate_images(self) -> None:
        for _ in range(self.COUNT):
            self.__generate_random_img_and_convert_to_grayscale()

    async def generate_images_async(self) -> None:
        tasks = [
            asyncio.to_thread(self.__generate_random_img_and_convert_to_grayscale)
            for _ in range(self.COUNT)
        ]
        await asyncio.gather(*tasks)

    def __generate_random_img_and_convert_to_grayscale(self) -> None:
        img = []
        width, height = self.TEST_IMG_SIZE

        print(f"Generating random image: {self.TEST_IMG_SIZE}")
        for _ in range(height):
            row = []
            for _ in range(width):
                # Using a list, so the value can be modified later.
                pixel_rgb = [random.randint(0, 255) for _ in range(3)]
                row.append(pixel_rgb)
            img.append(row)

        print("Random image generated. Converting to grayscale...")
        self.__convert_to_grayscale(img)

        print("Converted.")

    def __convert_to_grayscale(self, img: List[List[List]]) -> None:
        for row in img:
            for pixel in row:
                self.__convert_pixel_to_grayscale(pixel)

    def __convert_pixel_to_grayscale(self, pixel_rgb: list) -> None:
        new_value = round(sum(pixel_rgb) / len(pixel_rgb))
        for i, _ in enumerate(pixel_rgb):
            pixel_rgb[i] = new_value


def main(task_type: TaskType) -> None:
    print(f"Running synchronous {task_type}-bound task...")
    if task_type == TaskType.io:
        task = IOBound()
        task.download_pages()
    else:
        task = CPUBound()
        task.generate_images()


async def main_async(task_type: TaskType) -> None:
    print(f"Running asynchronous {task_type}-bound task...")
    if task_type == TaskType.io:
        task = IOBound()
        await task.download_pages_async()
    else:
        task = CPUBound()
        await task.generate_images_async()


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

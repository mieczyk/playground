from contextlib import contextmanager
import logging
import os
import time
from typing import List, Tuple
from PIL import Image

LOG_FILE_NAME = "orders.log"
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO)


@contextmanager
def measure_execution_time():
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Operation completed in {elapsed:0.2f} seconds.")


def get_logger(file_path: str) -> logging.Logger:
    return logging.getLogger(os.path.basename(file_path))


def display_image(img_data: List[List[List]], img_size: Tuple[int, int]) -> None:
    """
    Helps to verify randomly generated images.
    """
    flat_pixels = [tuple(pixel) for row in img_data for pixel in row]
    img = Image.new("RGB", img_size)
    img.putdata(flat_pixels)
    img.show()

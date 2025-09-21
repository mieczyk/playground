from contextlib import contextmanager
import logging
import os
import time


LOG_FILE_NAME = "orders.log"
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.INFO)


@contextmanager
def measure_execution_time():
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Orders completed in {elapsed:0.2f} seconds.")


def get_logger(file_path: str) -> logging.Logger:
    return logging.getLogger(os.path.basename(file_path))

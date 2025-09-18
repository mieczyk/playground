from contextlib import contextmanager
import time


@contextmanager
def measure_execution_time():
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"Orders completed in {elapsed:0.2f} seconds.")

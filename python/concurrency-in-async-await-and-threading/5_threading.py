# Simple example of concurrency with threading instead of asyncio.
import threading
import time
from utils import measure_execution_time


def make_burger(order_num: int) -> None:
    print(f"Preparing burger #{order_num}...")
    time.sleep(5)
    print(f"Burger made #{order_num}")


def main():
    order_queue = []
    for i in range(1, 4, 1):
        task = threading.Thread(target=make_burger, args=(i,))
        order_queue.append(task)
        task.start()

    # Wait for all "threads" to be finished.
    for task in order_queue:
        task.join()


if __name__ == "__main__":
    with measure_execution_time():
        main()

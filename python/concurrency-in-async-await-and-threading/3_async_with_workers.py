import asyncio

from utils import measure_execution_time


class Staff:
    def __init__(self, name: str):
        self.name = name

    async def prepare_meal(self, orders: asyncio.Queue) -> None:
        while orders.qsize() > 0:
            dish_name = await orders.get()
            print(f"[{self.name}] Preparing {dish_name}...")
            await asyncio.sleep(5)
            print(f"[{self.name}] {dish_name} is ready!")


class Kitchen:
    def __init__(self, max_orders_count: int):
        # `asyncio.Queue` is designed to work with async/await code.
        # If the queue is full, `await put()` blocks the code execution until an item is removed by `get()`.
        # If the queue is empty, `await get()` waits until an element is added to the queue by `put()`.
        # There are also non-blocking operaionts available:
        #   * `put_nowait()` - raises `QueueFull` if the queue is full.
        #   * `get_nowait()` - raises `QueueEmpty` if the queue is empty.
        # `asyncio.Queue` IS NOT THREAD-SAFE!
        self.orders = asyncio.Queue(max_orders_count)
        self.workers = []

    def add_worker(self, worker: Staff) -> None:
        self.workers.append(worker)

    def place_order(self, dish_name: str) -> None:
        # If the queue is full it raises the QueueFull exception instead of waiting.
        self.orders.put_nowait(dish_name)

    async def start_cooking(self) -> None:
        await asyncio.gather(
            *[worker.prepare_meal(self.orders) for worker in self.workers]
        )


async def main():
    # In the example we've got 4 dishes to prepare and 2 workers.
    # Cooking a single dish takes 5 seconds. With only one worker, it would take 20 seconds.
    # With 2 workers, it takes 10 seconds to prepare 4 dishes.
    kitchen = Kitchen(100)

    kitchen.add_worker(Staff("John"))
    kitchen.add_worker(Staff("Jane"))

    kitchen.place_order("Burger")
    kitchen.place_order("Pizza")
    kitchen.place_order("Fish")
    kitchen.place_order("French fries")

    await kitchen.start_cooking()


if __name__ == "__main__":
    with measure_execution_time():
        asyncio.run(main())

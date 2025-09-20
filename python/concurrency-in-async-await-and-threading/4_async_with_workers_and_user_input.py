import asyncio
from utils import measure_execution_time

# dish_name: preparation_time_in_seconds
DISHES = {"burger": 5, "fries": 2, "fish": 10, "pizza": 6}
SELECT_DISH_PROMPT = f"What would you like to order ({'|'.join(DISHES.keys())})?"


orders = asyncio.Queue()


def is_dish_in_menu(dish_name: str) -> bool:
    return dish_name in DISHES.keys()


class Staff:
    def __init__(self, name: str):
        self.name = name

    async def prepare_ordered_meal(self) -> None:
        while True:
            # If the orders queue is empty, it'll wait for the first element.
            dish_name = await orders.get()

            if not is_dish_in_menu(dish_name):
                break

            preparation_time_in_seconds = DISHES[dish_name]
            print(
                f"[{self.name}] Preparing {dish_name}. Will take {preparation_time_in_seconds} s..."
            )
            await asyncio.sleep(preparation_time_in_seconds)
            print(f"[{self.name}] {dish_name} is ready!")
        print(f"Preparing meals finished by {self.name}!")


async def take_orders(workers_number: int) -> None:
    while True:
        dish_name = await asyncio.to_thread(input, SELECT_DISH_PROMPT)
        if is_dish_in_menu(dish_name):
            orders.put_nowait(dish_name)
        else:
            # A little trick that puts a message to the queue for ALL running workers, so they all can stop working.
            # If we put only a single "stopper" message to the queue, only the first worker that reads the message will stop working.
            # Others will waiting forever for new orders in the queue.
            for _ in range(workers_number):
                orders.put_nowait("exit")
            break
    print("The kitchen is closed now!")


async def main() -> None:
    john = Staff("John")
    jane = Staff("Jane")

    # Run all awaitable objects passed to the method *concurrently* and waits
    # untill all tasks are done.
    await asyncio.gather(
        take_orders(2), john.prepare_ordered_meal(), jane.prepare_ordered_meal()
    )


if __name__ == "__main__":
    with measure_execution_time():
        asyncio.run(main())

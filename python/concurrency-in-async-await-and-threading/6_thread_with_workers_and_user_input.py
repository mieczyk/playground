import threading
import time
from utils import LOG_FILE_NAME, get_logger, measure_execution_time

# dish_name: preparation_time_in_seconds
DISHES = {"burger": 5, "fries": 2, "fish": 10, "pizza": 6}
SELECT_DISH_PROMPT = f"What would you like to order ({'|'.join(DISHES.keys())})? "

logger = get_logger(__file__)

# Resource with protected access (lock) containing ordered dishes to prepare.
orders_queue = []

# Flag determining if staff tasks (preparing meals) should be stopped.
kitchen_open = True

# To avoid race conditions, the tasks queue access should be protected
# by threads synchronization mechnisms (e.g. simple lock).
queue_lock = threading.Lock()


class Staff:
    def __init__(self, name: str):
        self.name = name

    def prepare_ordered_meal(self) -> None:
        while True:
            dish_name = None
            with queue_lock:
                if len(orders_queue) == 0:
                    if not kitchen_open:
                        break
                else:
                    dish_name = orders_queue.pop(0)

            if dish_name is not None:
                self.__cook_the_dish(dish_name)
            else:
                time.sleep(1)  # Wait for an order.

        logger.info(f"Preparing meals finished by {self.name}!")

    def __cook_the_dish(self, dish_name: str) -> None:
        preparation_time_in_seconds = DISHES[dish_name]
        logger.info(
            f"[{self.name}] Preparing {dish_name}. Will take {preparation_time_in_seconds} s..."
        )
        time.sleep(preparation_time_in_seconds)
        logger.info(f"[{self.name}] {dish_name} is ready!")


def take_orders():
    # We need to explicitly mark the variable as global if we want to change its value
    # inside a function.
    global kitchen_open
    while True:
        dish_name = input(SELECT_DISH_PROMPT)
        if dish_name in DISHES.keys():
            with queue_lock:
                orders_queue.append(dish_name)
            logger.info(f"Ordered: {dish_name}")
        else:
            kitchen_open = False
            break
    logger.info("The kitchen is closed now! No more orders will be accepted.")


def main():
    waiter_task = threading.Thread(target=take_orders, name="Waiter")
    waiter_task.start()

    john = Staff("John")
    john_task = threading.Thread(target=john.prepare_ordered_meal, name="John")
    john_task.start()

    jane = Staff("Jane")
    jane_task = threading.Thread(target=jane.prepare_ordered_meal, name="Jane")
    jane_task.start()

    # Wait for all tasks to finish
    waiter_task.join()
    john_task.join()
    jane_task.join()

    print(f"Check the {LOG_FILE_NAME} file for ordered meals list.")


if __name__ == "__main__":
    with measure_execution_time():
        main()

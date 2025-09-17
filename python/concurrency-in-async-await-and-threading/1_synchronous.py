import time

from utils import measure_execution_time

def make_burger(order_num: int) -> None:
    print(f"Preparing burger #{order_num}...")
    time.sleep(5) # Blocking operation
    print(f"Burger made #{order_num}")


def main():
    for i in range(1, 4, 1):
        make_burger(i)


if __name__ == "__main__":
    # Each task is performed synchronously, so it will take ~15 seconds.
    with measure_execution_time():
        main()
import time

def make_burger(order_num: int) -> None:
    print(f"Preparing burger #{order_num}...")
    time.sleep(5) # Blocking operation
    print(f"Burger made #{order_num}")


def main():
    for i in range(1, 4, 1):
        make_burger(i)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start

    print(f"Orders completed in {elapsed:0.2f} seconds.")
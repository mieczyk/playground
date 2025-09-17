import asyncio
import time


async def make_burger(order_num: int) -> None:
    print(f"Preparing burger #{order_num}...")
    # Non-blocking operation.
    # Until the async sleep function completes (I/O operation), another coroutine is working.
    await asyncio.sleep(5) 
    print(f"Burger made #{order_num}")

async def main():
    order_queue = []
    for i in range(1, 4, 1):
        order_queue.append(make_burger(i))
    # Wait until all asynchronous tasks are finished.
    await asyncio.gather(*order_queue)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start

    # Should take ~5 seconds. The `make_burger` coroutines are working concurrently.
    print(f"Orders completed in {elapsed:0.2f} seconds.")
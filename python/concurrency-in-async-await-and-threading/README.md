# Source
Scripts and notes from the article: [Faster Python: Concurrency in async/await and threading](https://blog.jetbrains.com/pycharm/2025/06/concurrency-in-async-await-and-threading/#).

# Hightlights
- Due to the limitation of GIL (Global Interpreter Lock), *multithreading* in Python works on a single core only (except for the *nogil Python* implementation).
- In `threading` the operating system's manager decides what thread is running. In `async/await` a currently running coroutine passes control to another waiting coroutine if a blocing operation occurs.
- Couroutines in Python are actually generators that are able to pause and pass back to the main function. `async/await` is possible because of them.
- As both `4_async_with_workers_and_user_input.py` and `6_thread_with_workers_and_user_input.py` scripts show, we can achieve the same results with `threading` and `asyncio` if we deal with I/O-bound tasks. However, coding with `asyncio` is easier as we don't have to take care of potential race conditions and deadlocks by ourselves. Controls are passed around coroutines by default, so no locks are needed.
- The `async/await` concurrency is able to optimize only I/O-bound tasks (e.g. reading from a file or network, waiting for a user's input), especially with GIL Python. If there's a task that needs waiting for an I/O operation to complete, the CPU (core or a processor) is not occupied and can run another task in the meantime.
- In case of CPU-bound tasks that keep the CPU busy (e.g. complex math calculations, training machine learning models, processing images/videos etc.), the `async/await` concurrency is pretty useless. If we want to run tasks truely simultaneously, using multiple cores or CPUs, we should consider using the [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) package, so we can work around the GIL limitations.
- Python 3.13 allows us to disable GIL.

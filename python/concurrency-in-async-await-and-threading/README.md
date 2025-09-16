# Source
Scripts and notes from the article: [Faster Python: Concurrency in async/await and threading](https://blog.jetbrains.com/pycharm/2025/06/concurrency-in-async-await-and-threading/#).

# Hightlights
- Due to the limitation of GIL (Global Interpreter Lock), *multithreading* in Python works on a single core only (except for the *nogil Python* implementation).
- In `threading` the operating system's manager decides what thread is running. In `async/await` a currently running coroutine passes control to another waiting coroutine if a blocing operation occurs.
- Couroutines in Python are actually generators that are able to pause and pass back to the main function. `async/await` is possible because of them.

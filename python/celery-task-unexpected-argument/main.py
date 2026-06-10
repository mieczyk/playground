# PoC that shows whether a Celery task fails if called with additional, unexpected argument.
# * The `poc.make_coffee` task fails as it doesn't expect any other params that `coffee_type`.
# * The `poc.make_tea` task succeeds as it accepts variable number of keyword arguments (**kwargs).

# Run the handler worker:
#   uv run python -m celery -A main:handler_app worker

# Send the tasks:
#   uv run pyhon main.py

from celery import Celery

task_routes = {"poc.*": {"queue": "poc"}}

sender_app = Celery("sender_app", broker="amqp://guest@localhost//")
handler_app = Celery("handler_app", broker="amqp://guest@localhost//")

@handler_app.task(name="poc.make_coffee")
def make_coffee(coffe_type: str):
    print(f"Making coffee: {coffe_type}")

@handler_app.task(name="poc.make_tea")
def make_tea(tea_type: str, **kwargs):
    print(f"Making tea: {tea_type}")
    print(f"Additional params for tea: {kwargs}")

if __name__ == "__main__":
    print(f"[*] Calling {make_coffee} task")
    sender_app.send_task("poc.make_coffee", kwargs={"coffe_type": "espresso", "unexpected": "whatever"})

    print(f"[*] Calling {make_tea} task.")
    sender_app.send_task("poc.make_tea", kwargs={"tea_type": "green", "unexpected": "whatever"})
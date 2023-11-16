# To run the server (from the directory containing the app.py file):
#   poetry run uvicorn app:app --reload

# uvicorn - ASGI web server (https://www.uvicorn.org/).
# --reload - automatically reload app after each change.

from fastapi import FastAPI

from fastapi_custom_middleware.middleware import (
    RateLimitMiddleware, another_middleware_function,
    set_timestamp_on_request_and_response)

app = FastAPI()


# Define endpoints
@app.get("/info")
async def info(timestamp: int = None):
    return {"msg": f"My first FastAPI application: {timestamp}"}


@app.get("/v2/info")
async def info_v2():
    return {"msg": "Version 2 of my first application"}


# Register middleware components
app.middleware("http")(set_timestamp_on_request_and_response)
app.middleware("http")(another_middleware_function)
app.add_middleware(RateLimitMiddleware)

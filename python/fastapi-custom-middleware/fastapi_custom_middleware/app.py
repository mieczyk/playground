# To run the server (from the directory containing the app.py file): 
#   poetry run uvicorn app:app --reload

# uvicorn - ASGI web server (https://www.uvicorn.org/).
# --reload - automatically reload app after each change.

from fastapi import FastAPI

app = FastAPI()

# Returns a "JSONResponse" object.
@app.get("/info")
async def info():
    return { "msg": "My first FastAPI application" }

@app.get("/v2/info")
async def info_v2():
    return { "msg": "Version 2 of my first application" }
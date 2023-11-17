Proof of concept based on the [Building Custom Middleware in FastAPI](https://semaphoreci.com/blog/custom-middleware-fastapi) article.
It shows how to build custom middleware (both function-based and class-based) and use it to modify requests and responses.

# TLDR

FastAPI built-in middleware components:
- **CORSMiddleware** - includes CORS headers in responses.
- **TrustedHostMiddleware** - validates the `Host` header of incoming requests to prevent [HTTP Host header attacks](https://portswigger.net/web-security/host-header).
- **SessionMiddleware** - signed cookie-based session.
- **GZip Middleware** - helps to reduce bandwidth usage by compressing response payloads.

A `Request` has a `request.scope` attribute, that's just a Python `dict` containing the metadata related to the request.

Middleware components are executed in the order they are registered and the registration order is reversed compared to how we define them. In other words: **the last function/class registered is the first one to run and handle a request** (responses are handled in the reverse order, of course).

In order to test FastAPI endpoints, the built-in `fastapi.testclient.TestClient` class can be used.

Things that should be kept in mind while using middleware components:
- Middleware should lightweight as it's executed before each request and after each response.
- Middleware components order matter.
- Keep middleware documentation up-to-date, so handling requests/responses doesn't look like a magic for newcomers.

How to apply custom logging configuration to Uvicorn: [FastAPI and Uvicorn Logging](https://gist.github.com/liviaerxin/d320e33cbcddcc5df76dd92948e5be3b).

# PoC

## API endpoints

Very simple FastAPI application that demonstrates custom middleware's behavior. It exposes only two endpoints that do nothing except returning a JSON formatted message:
- `/info`
- `/v2/info`

## Middleware

- `RateLimitMiddleware` - class-based middleware definition responsible for rate limiting (max 10 requests per second).
- `set_timestamp_on_request_and_response` - function-based middleware that automatically adds current timestamp to each request as a query parameter and adds the same timestamp to each response as a HTTP header (`X-Timestamp`).
- `another_middleware_function` - function-based middleware that does nothing. Its purpose is to show the middleware components' execution order.

## Setup

Install all required dependencies:

```
poetry install
```

Run the server (from the directory containing the this README file):

```
poetry run uvicorn fastapi_custom_middleware.app:app --reload --log-config=logging.yml
```

`--reload` option automatically reloads the app after each change.

Run the tests:

```
poetry run pytest tests/
```
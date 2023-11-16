# Overview

Proof of concept based on the [Building Custom Middleware in FastAPI](https://semaphoreci.com/blog/custom-middleware-fastapi) article.
It shows how to build custom middleware (both function-based and class-based) and use it to modify requests and responses.

## TLDR

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
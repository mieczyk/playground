# Overview

Proof of concept based on the [Building Custom Middleware in FastAPI](https://semaphoreci.com/blog/custom-middleware-fastapi) article.

## Summary

FastAPI built-in middleware components:
- **CORSMiddleware** - includes CORS headers in responses.
- **TrustedHostMiddleware** - validates the `Host` header of incoming requests to prevent [HTTP Host header attacks](https://portswigger.net/web-security/host-header).
- **SessionMiddleware** - signed cookie-based session.
- **GZip Middleware** - helps to reduce bandwidth usage by compressing response payloads.

# TODO:
Problem to resolve: `ModuleNotFoundError: No module named 'fastapi'`
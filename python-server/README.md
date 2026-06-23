# HTTP Server From Scratch

A simple, lightweight HTTP server implemented from scratch in Python using low-level sockets.

## Objective
Build a custom HTTP server without using high-level web frameworks or built-in HTTP servers (like `http.server`). It directly handles TCP sockets, parses raw HTTP bytes, maps requests to handlers, and constructs valid HTTP responses.

## Current Support & Features
- **TCP Socket Server**: Listens on `127.0.0.1:9999` using Python's standard `socket` library.
- **Request Parsing**: Extracts HTTP method, URI, and version from incoming connection streams.
- **Dynamic Routing/Dispatching**: Dynamically maps HTTP methods to handlers (e.g., `handle_GET`).
- **Static File Serving**: Serves files from the `html/` directory and auto-detects MIME types using the `mimetypes` library.
- **Directory Traversal Protection**: Ensures requests cannot access files outside the `html/` folder using path resolution checks.
- **Status Codes Supported**:
  - `200 OK`: Successful file retrieval.
  - `404 Not Found`: Triggered for missing files. Serves custom `404.html` if available.
  - `405 Method Not Allowed`: Triggered for unsupported HTTP methods (any method other than `GET`). Serves custom `405.html` if available.
  - `500 Internal Server Error`: Catch-all for server errors. Serves custom `500.html` if available.

## How to Run
Run the server using Python:
```bash
python server.py
```
Then visit: `http://127.0.0.1:9999/`

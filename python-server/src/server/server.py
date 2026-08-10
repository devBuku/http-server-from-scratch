import socket

from .handler import FileHandler
from .request import Request
from .response import Response


class HTTPServer(FileHandler):
    def __init__(self, host="127.0.0.1", port=9999, base_dir="html"):
        super().__init__(base_dir)
        self.host = host
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        print(f"Go to http://{self.host}:{self.port}")

        while True:
            conn, address = server_socket.accept()

            try:
                data = conn.recv(4096)
                if not data:
                    continue
                request = Request(data)
                response = self.dispatch(request)
                conn.sendall(response.build_response())
            except Exception as e:
                print(f"Error: {e}")
                internal_error_path = self.base_dir / "500.html"
                if internal_error_path.exists() and not internal_error_path.is_dir():
                    body = self.read_file(internal_error_path)
                    response = Response(
                        status_code=500,
                        body=body,
                        headers={"Content-Type": "text/html"},
                    )
                else:
                    response = Response(
                        status_code=500,
                        body=b"<h1>500 Internal Server Error</h1>",
                        headers={"Content-Type": "text/html"},
                    )
                conn.sendall(response.build_response())
            finally:
                conn.close()

    def dispatch(self, request: Request):
        handler_name = f"handle_{request.method}"
        handler = getattr(self, handler_name, self.handle_405)
        return handler(request)

    def handle_GET(self, request: Request):
        return self.serve_file(request.uri)

    def handle_405(self, request: Request):
        return Response(
            status_code=405,
            body=b"<h1>405 Method Not Allowed</h1>",
            headers={"Content-Type": "text/html"},
        )


if __name__ == "__main__":
    server = HTTPServer()
    server.start()

import socket
import mimetypes
from pathlib import Path
from datetime import datetime, timezone


class Request:
    def __init__(self, data: bytes):
        self.data = data
        self.method = None
        self.uri = None
        self.http_version = None
        self.parse()

    def parse(self):
        request_line = self.data.splitlines()[0] if self.data else b""
        parts = request_line.decode().split(" ")

        self.method = parts[0]
        if len(parts) > 1:
            self.uri = parts[1]
        else:
            self.uri = "/"
        if len(parts) > 2:    
            self.http_version = parts[2]  
        else:
            self.http_version = "HTTP/1.1"

class Response:
    status_codes = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error",
        405: "Method Not Allowed"
    }

    def __init__(self, status_code=200, body=b"", headers=None):
        self.status_code = status_code
        self.body = body
        self.headers = headers or {}

    @staticmethod
    def get_date():
        dt = datetime.now(timezone.utc)
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")

    def build_response(self):
        status_line = (f"HTTP/1.1 {self.status_code} " f"{self.status_codes[self.status_code]}\r\n")

        default_headers = {"Server": "HelloFriendServer", "Date": self.get_date(), "Content-Length": str(len(self.body))}

        default_headers.update(self.headers)

        header_block = ""

        for key, value in default_headers.items():
            header_block += f"{key}: {value}\r\n"

        return (status_line.encode() + header_block.encode() + b"\r\n" + self.body)


class FileHandler:
    def __init__(self, base_dir="html"):
        self.base_dir = Path(base_dir)
    def read_file(self, file_path: Path):
        try:
            resolved_path = file_path.resolve()
            base_path = self.base_dir.resolve()

            if not resolved_path.is_relative_to(base_path):
                return None

            if not resolved_path.exists():
                return None

            if resolved_path.is_dir():
                return None

            with open(resolved_path, "rb") as f:
                return f.read()

        except Exception:
            return None
    def serve_file(self, path: str):
        if path == "/":
            file_path = self.base_dir / "index.html"
        else:
            file_path = self.base_dir / path.strip("/")

        if not file_path.exists() or file_path.is_dir():
            not_found_path = self.base_dir / "404.html"
            if not_found_path.exists() and not not_found_path.is_dir():
                body = self.read_file(not_found_path)
                return Response(status_code=404,body=body,headers={"Content-Type": "text/html"})
            return Response(status_code=404,body=b"<h1>404 Not Found</h1>",headers={"Content-Type": "text/html"})
        content_type = mimetypes.guess_type(str(file_path))[0]
        content_type = content_type or "application/octet-stream"
        try:
            body = self.read_file(file_path)
            return Response(status_code=200,body=body,headers={"Content-Type": content_type})
        except Exception:
            internal_error_path = self.base_dir / "500.html"
            if internal_error_path.exists() and not internal_error_path.is_dir():
                body = self.read_file(internal_error_path)
                return Response(status_code=500,body=body,headers={"Content-Type": "text/html"})
        

class HTTPServer(FileHandler):
    def __init__(self, host="127.0.0.1", port=9999, base_dir="html"):
        super().__init__(base_dir)
        self.host = host
        self.port = port
        

    def start(self):
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        print(f"Go to http://{self.host}:{self.port}")

        while True:
            conn,address = server_socket.accept()
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
                    response = Response(status_code=500,body=body,headers={"Content-Type": "text/html"})
                else:
                    response = Response(status_code=500,body=b"<h1>500 Internal Server Error</h1>",headers={"Content-Type": "text/html"})
                conn.sendall(response.build_response())
            finally:
                conn.close()

    def dispatch(self, request: Request):
        handler_name = f"handle_{request.method}"
        handler = getattr(self,handler_name,self.handle_405)
        return handler(request)

    def handle_GET(self, request: Request):
        return self.serve_file(request.uri)

    def handle_405(self, request: Request):
        return Response(status_code=405,body=b"<h1>405 Method Not Allowed</h1>",headers={"Content-Type": "text/html"})


if __name__ == "__main__":
    server = HTTPServer()
    server.start()
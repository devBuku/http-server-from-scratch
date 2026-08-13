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

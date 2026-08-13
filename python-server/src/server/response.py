from datetime import datetime, timezone


class Response:
    status_codes = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error",
        405: "Method Not Allowed",
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
        status_line = (
            f"HTTP/1.1 {self.status_code} " f"{self.status_codes[self.status_code]}\r\n"
        )

        default_headers = {
            "Server": "HelloFriendServer",
            "Date": self.get_date(),
            "Content-Length": str(len(self.body)),
        }

        default_headers.update(self.headers)

        header_block = ""

        for key, value in default_headers.items():
            header_block += f"{key}: {value}\r\n"

        return status_line.encode() + header_block.encode() + b"\r\n" + self.body

import mimetypes
from pathlib import Path
from .response import Response


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
                return Response(
                    status_code=404, body=body, headers={"Content-Type": "text/html"}
                )
            return Response(
                status_code=404,
                body=b"<h1>404 Not Found</h1>",
                headers={"Content-Type": "text/html"},
            )
        content_type = mimetypes.guess_type(str(file_path))[0]
        content_type = content_type or "application/octet-stream"
        try:
            body = self.read_file(file_path)
            return Response(
                status_code=200, body=body, headers={"Content-Type": content_type}
            )
        except Exception:
            internal_error_path = self.base_dir / "500.html"
            if internal_error_path.exists() and not internal_error_path.is_dir():
                body = self.read_file(internal_error_path)
                return Response(
                    status_code=500, body=body, headers={"Content-Type": "text/html"}
                )

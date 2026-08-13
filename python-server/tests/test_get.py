import unittest
import tempfile
import shutil
from pathlib import Path

from src.server.request import Request
from src.server.handler import FileHandler


class TestGetEndpoint(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.base_dir = Path(self.test_dir)

        (self.base_dir / "index.html").write_text("<h1>Index</h1>")
        (self.base_dir / "test.txt").write_text("Hello World")
        (self.base_dir / "404.html").write_text("<h1>404 Not Found</h1>")

        self.handler = FileHandler(base_dir=str(self.base_dir))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_request_parsing_get(self):
        req = Request(b"GET /test.txt HTTP/1.1\r\n\r\n")
        self.assertEqual(req.method, "GET")
        self.assertEqual(req.uri, "/test.txt")

    def test_serve_root(self):
        response = self.handler.serve_file("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b"<h1>Index</h1>")
        self.assertEqual(response.headers["Content-Type"], "text/html")

    def test_serve_existing_file(self):
        response = self.handler.serve_file("/test.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b"Hello World")
        self.assertEqual(response.headers["Content-Type"], "text/plain")

    def test_serve_non_existent_file_returns_404(self):
        response = self.handler.serve_file("/missing.html")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.body, b"<h1>404 Not Found</h1>")


if __name__ == "__main__":
    unittest.main()

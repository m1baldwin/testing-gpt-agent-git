"""Exercise the real HTTP server on an ephemeral loopback port."""

import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

from server import create_server


class ServerTests(unittest.TestCase):
    def test_loopback_greeting_and_missing_page(self):
        with create_server(0) as server:
            self.assertEqual(server.server_address[0], "127.0.0.1")
            worker = threading.Thread(target=server.serve_forever)
            worker.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}"
                with urlopen(url + "/", timeout=2) as response:
                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.headers.get_content_type(), "text/html")
                    self.assertIn(b"<h1>hello world</h1>", response.read())
                with self.assertRaises(HTTPError) as missing:
                    urlopen(url + "/missing", timeout=2)
                self.assertEqual(missing.exception.code, 404)
            finally:
                server.shutdown()
                worker.join(timeout=2)


if __name__ == "__main__":
    unittest.main()

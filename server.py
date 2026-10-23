"""Serve a greeting on IPv4 loopback using only Python's standard library."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8000
PAGE = b"<!doctype html><html lang='en'><meta charset='utf-8'><title>Hello world</title><h1>hello world</h1></html>"


class GreetingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(PAGE)))
        self.end_headers()
        self.wfile.write(PAGE)


def create_server(port=PORT):
    return ThreadingHTTPServer((HOST, port), GreetingHandler)


def main():
    with create_server() as server:
        print(f"Open http://{HOST}:{PORT}/ (Ctrl+C to stop)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()

"""Serve a greeting on IPv4 loopback using only Python's standard library."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8000
PAGE = b"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Hello world</title>
  <style>
    body { font-family: system-ui, sans-serif; text-align: center; padding: 4rem 1rem; }
    h1 { display: inline-block; color: #174ea6; }
    button { display: block; margin: 1.5rem auto; padding: .7rem 1.2rem;
             font: inherit; cursor: pointer; }
  </style>
</head>
<body>
  <h1>hello world</h1>
  <button type="button" id="play">Play hello world</button>
  <p id="status" role="status">Ready to say hello.</p>
  <script>
    const greeting = document.querySelector('h1');
    const button = document.querySelector('#play');
    const status = document.querySelector('#status');
    button.addEventListener('click', async () => {
      button.disabled = true;
      status.textContent = 'Saying hello...';
      const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
      const frames = reducedMotion
        ? [{ opacity: 0.5 }, { opacity: 1 }]
        : [
            { transform: 'translateY(0) rotate(0deg) scale(1)' },
            { transform: 'translateY(-24px) rotate(-8deg) scale(1.15)', offset: 0.35 },
            { transform: 'translateY(-12px) rotate(8deg) scale(1.1)', offset: 0.65 },
            { transform: 'translateY(0) rotate(0deg) scale(1)' }
          ];
      try {
        await greeting.animate(frames, {
          duration: reducedMotion ? 200 : 900, easing: 'ease-in-out'
        }).finished;
        status.textContent = 'Hello again! Play it again whenever you like.';
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>"""


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

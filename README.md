# Git agent workflow test

This repository tests personal agent instructions and the shared `agent-git`
wrapper through a small, reviewable Python project.

The initial feature serves “hello world” locally on loopback only. It will be
submitted as a pull request to `main` for human review and merge. After that
merge is confirmed, a separate pull request will add and test a button that
plays a short hello-world animation.

## Run locally

Requires Python 3; no third-party packages are needed.

```sh
python3 server.py
```

Open http://127.0.0.1:8000/ in your browser. Stop with Ctrl+C.
The server binds explicitly to `127.0.0.1`, so other computers cannot connect
directly. Port 8000 must be available. This is a local development server.

## Test

```sh
python3 -m unittest -v
```

The test starts a real HTTP server on a temporary loopback port and checks the
bind address, greeting response, HTML content type, and missing-page response.

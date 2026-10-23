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
directly. Click **Play hello world** to make the greeting bounce and wave.
You can replay it after it finishes. With reduced motion enabled in your system
or browser, the greeting uses a brief fade instead.

Port 8000 must be available. This is a local development server.

## Test

```sh
python3 -m unittest -v
```

The test starts a real HTTP server on a temporary loopback port and checks the
bind address, greeting response, HTML content type, and missing-page response.

For the optional browser check, install Playwright into a temporary directory
(requires Node.js/npm), then run with `python3 server.py` in another terminal:

```sh
npm install --prefix /tmp/hello-world-browser playwright
/tmp/hello-world-browser/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/hello-world-browser/node_modules node test_browser.cjs
```

This checks button clicks, visible animation, completion, and replay with both
normal and reduced motion, and fails on browser JavaScript errors.

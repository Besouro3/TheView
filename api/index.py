import os
import socket
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

import streamlit.web.bootstrap as bootstrap

STREAMLIT_PORT = 8501


def _run_streamlit() -> None:
    # signal handlers can only be installed from the main thread, so we disable
    # them for the background Streamlit server.
    bootstrap._set_up_signal_handler = lambda server: None
    bootstrap.run(
        str(ROOT / "app.py"),
        is_hello=False,
        args=[],
        flag_options={
            "server.address": "0.0.0.0",
            "server.port": str(STREAMLIT_PORT),
            "server.headless": "true",
            "browser.gatherUsageStats": "false",
        },
    )


_thread = threading.Thread(target=_run_streamlit, daemon=True)
_thread.start()


def _server_up() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", STREAMLIT_PORT), timeout=0.5):
            return True
    except OSError:
        return False


def _wait_ready(timeout: float = 30.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _server_up():
            return
        time.sleep(0.25)


import requests as http
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import StreamingResponse

UPSTREAM = f"http://127.0.0.1:{STREAMLIT_PORT}"


async def proxy(request: Request) -> StreamingResponse:
    _wait_ready()
    url = UPSTREAM + request.url.path
    if request.url.query:
        url = f"{url}?{request.url.query}"
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    body = await request.body() if request.method in ("POST", "PUT", "PATCH") else None
    resp = http.request(
        request.method,
        url,
        headers=headers,
        data=body,
        stream=True,
        timeout=45,
        allow_redirects=False,
    )
    return StreamingResponse(
        resp.iter_content(chunk_size=65536),
        status_code=resp.status_code,
        headers=dict(resp.headers),
    )


app = Starlette()


async def catch_all(request: Request, path: str) -> StreamingResponse:
    return await proxy(request)


app.add_route("/{path:path}", catch_all, methods=["GET", "POST", "PUT", "PATCH", "DELETE"])

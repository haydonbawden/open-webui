"""
Executable entrypoint for the Windows one-file build.

This module ensures we run with the same environment assumptions as
``open_webui.__init__.serve`` while also supporting PyInstaller's
``sys._MEIPASS`` extraction directory.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _prepare_environment() -> None:
    """Prepare runtime environment for the bundled executable.

    When PyInstaller runs in one-file mode it extracts the application into a
    temporary directory that is exposed as ``sys._MEIPASS``. We mirror that
    location into ``BASE_DIR`` so existing path logic can resolve bundled
    assets like the frontend build and static files. We also enable the
    ``FROM_INIT_PY`` flag so ``open_webui.env`` points to the packaged
    frontend folder under ``open_webui/frontend``.
    """

    if getattr(sys, "frozen", False):
        base_path = Path(getattr(sys, "_MEIPASS"))
        os.environ.setdefault("BASE_DIR", str(base_path))

    os.environ.setdefault("FROM_INIT_PY", "true")


def main() -> None:
    _prepare_environment()

    from open_webui.__init__ import serve

    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))

    serve(host=host, port=port)


if __name__ == "__main__":  # pragma: no cover - runtime entrypoint
    main()

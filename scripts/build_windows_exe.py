"""Helper script for producing the Windows one-file executable.

This script expects that ``npm run build`` has already produced the frontend
assets in ``/build``. It copies those assets into the Python package so the
PyInstaller spec can bundle them, then invokes PyInstaller using the checked-in
``windows-onefile.spec``.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_BUILD = PROJECT_ROOT / "build"
PACKAGE_FRONTEND = PROJECT_ROOT / "backend" / "open_webui" / "frontend"
SPEC_PATH = PROJECT_ROOT / "scripts" / "windows-onefile.spec"


def _copy_frontend() -> None:
    if not FRONTEND_BUILD.exists():
        raise SystemExit(
            "Frontend build not found. Run `npm run build` before packaging."
        )

    if PACKAGE_FRONTEND.exists():
        shutil.rmtree(PACKAGE_FRONTEND)

    shutil.copytree(FRONTEND_BUILD, PACKAGE_FRONTEND)


def _run_pyinstaller() -> None:
    subprocess.run(
        [sys.executable, "-m", "PyInstaller", str(SPEC_PATH)], check=True
    )


if __name__ == "__main__":
    _copy_frontend()
    _run_pyinstaller()
    exe_path = PROJECT_ROOT / "dist" / "Open-WebUI.exe"
    print(f"\nBuilt executable: {exe_path}")

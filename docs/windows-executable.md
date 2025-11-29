# Windows standalone executable

The repository now ships with a PyInstaller-based flow that produces a single
self-contained Windows x64 executable. Python, dependencies, the backend, and
pre-built frontend assets are bundled together so the resulting `.exe` can run
without any external runtime installs.

## Building locally

1. Install Node.js 18+ and Python 3.11 on Windows.
2. Install Node dependencies and build the frontend:

   ```powershell
   npm install --force
   $env:APP_BUILD_HASH = git rev-parse HEAD
   npm run build
   ```

3. Install Python dependencies that are compatible with the PyInstaller build
   (a Windows-friendly subset lives in `backend/requirements-windows.txt`):

   ```powershell
   python -m pip install --upgrade pip
   pip install -r backend/requirements-windows.txt
   pip install pyinstaller
   ```

4. Package everything into a single executable. The helper script copies the
   frontend build into `backend/open_webui/frontend` and invokes PyInstaller
   using the checked-in spec file:

   ```powershell
   python scripts/build_windows_exe.py
   ```

5. The bundled binary is emitted at `dist/Open-WebUI.exe`.

## CI/CD automation

The GitHub Actions workflow `.github/workflows/release-windows-exe.yml` builds
and uploads the executable automatically whenever a release is published:

- Runs on `windows-latest` to match the target platform.
- Builds the frontend and injects the assets into the Python package.
- Installs the Windows-friendly backend dependencies and PyInstaller.
- Packages the one-file executable from the provided spec.
- Renames the binary to include the package version and attaches it to the
  release as an asset.

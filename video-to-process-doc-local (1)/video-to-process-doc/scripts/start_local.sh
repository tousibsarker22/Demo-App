#!/usr/bin/env bash
set -euo pipefail

# Backend venv
cd "$(dirname "$0")/.."
BACKEND_DIR=backend
FRONTEND_DIR=frontend

python3 -m venv "$BACKEND_DIR/.venv"
source "$BACKEND_DIR/.venv/bin/activate"
pip install --upgrade pip
pip install -r "$BACKEND_DIR/requirements.txt"

# Start backend
(   cd "$BACKEND_DIR" &&   export WORK_DIR=./data &&   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 ) &
BACK_PID=$!

echo "Backend started (PID $BACK_PID)"

# Frontend
pushd "$FRONTEND_DIR" >/dev/null
if [ ! -d node_modules ]; then
  npm install --legacy-peer-deps || yarn install || true
fi
export NEXT_PUBLIC_API_BASE=http://localhost:8000

# Open browser
python3 - <<'PY'
import webbrowser, time
url = 'http://localhost:3000'
for _ in range(10):
    time.sleep(0.5)
webbrowser.open(url)
PY

npm run dev
popd >/dev/null

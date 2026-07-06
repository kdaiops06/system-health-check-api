#!/usr/bin/env bash

set -euo pipefail

echo "==> Bootstrapping System Health Check API..."

if ! command -v python3.12 >/dev/null 2>&1; then
    echo "Error: Python 3.12 is required."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv .venv
fi

echo "Installing dependencies..."
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

echo ""
echo "Bootstrap completed successfully."
echo ""
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  make run"
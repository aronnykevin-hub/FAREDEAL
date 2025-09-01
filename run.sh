#!/usr/bin/env bash
set -euo pipefail

# Simple local runner for Fare Deal Supermarket
# Usage: ./run.sh

if ! command -v python3 >/dev/null 2>&1; then
	echo "python3 not found. Please install Python 3.10+" >&2
	exit 1
fi

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
	cp .env.example .env
	echo "Created .env from .env.example"
fi

# Prefer virtualenv if available
if python3 -m venv .venv 2>/dev/null; then
	. ./.venv/bin/activate
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt
else
	# Fallback to system pip (not recommended)
	python3 -m pip install --break-system-packages -r requirements.txt
fi

python3 run.py
#!/usr/bin/env bash

echo "Starting FluxForge Backend..."

gnome-terminal -- bash -c "
cd ~/projects/fluxforge/backend
source .venv/bin/activate
uv run uvicorn app.main:app --reload
exec bash
"

echo "Starting FluxForge Frontend..."

gnome-terminal -- bash -c "
cd ~/projects/fluxforge/frontend
npm run dev
exec bash
"

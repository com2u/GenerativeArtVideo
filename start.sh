#!/bin/bash

# Find system library paths and create symlinks if needed
LIBGL_PATH=$(find /usr/lib -name "libGL.so.1" 2>/dev/null | head -n 1)
LIBEGL_PATH=$(find /usr/lib -name "libEGL.so.1" 2>/dev/null | head -n 1)

if [ -n "$LIBGL_PATH" ] && [ ! -f "libGL.so" ]; then
    ln -sf "$LIBGL_PATH" libGL.so
fi

if [ -n "$LIBEGL_PATH" ] && [ ! -f "libEGL.so" ]; then
    ln -sf "$LIBEGL_PATH" libEGL.so
fi

# Set library path to include current directory for the symlinks
export LD_LIBRARY_PATH=".:$LD_LIBRARY_PATH"

# Ensure uv is installed
if ! command -v uv &> /dev/null
then
    echo "uv not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
. .venv/bin/activate

# Install requirements
echo "Installing requirements..."
uv pip install -r requirements.txt

# Start the app
echo "Starting the app..."
python main.py

#!/bin/bash

if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python3 to continue."
    exit 1
fi

PYTHON_CMD="python3"
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
fi

if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv py3.1venv
fi

if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source py3.1venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source py3.1venv/Scripts/activate
else
    echo "Unknown OS"
    exit 1
fi

if ! pip install -r requirements.txt; then
    echo "Failed to install dependencies."
    deactivate
    exit 1
fi

echo "Starting the server..."
python server.py &
SERVER_PID=$!
echo "Server started in the background. PID: $SERVER_PID"

deactivate

#!/bin/bash
# Dependencies setup and server run script

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 to continue."
    exit 1
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
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
echo "Server started in the background. PID: $!"
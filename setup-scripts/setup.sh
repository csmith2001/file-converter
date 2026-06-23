#!/usr/bin/env bash
set -e

OS="$(uname)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo
echo "Project Directory: $PROJECT_DIR"
echo "Script Directory: $SCRIPT_DIR"
echo
echo "Checking for Python Virtual Environment..."

# Check if python is installed
if ! python3 --version > /dev/null 2>&1; then
    echo "ERROR: python 3 is not installed!"
    echo "Install with:"
    echo "sudo apt install python3 python3-pip"
    exit 1
fi

# Check if venv is installed
if ! python3 -m venv --help > /dev/null 2>&1; then
    echo "ERROR: Python venv support is missing"
    echo

    if [ "$OS" = "Darwin" ]; then
        echo "Install with: brew install python"
    elif [ "$OS" = "Linux" ]; then
        echo "Install with: sudo apt install python3-venv"
    else
        echo "Install python3-venv for your system"
    fi

    exit 1
fi

# Check if .venv dir exists
if [ ! -d "${VENV_DIR}" ]; then
    echo "Creating .venv"
    python3 -m venv "$VENV_DIR"
else
    echo ".venv exists"
fi

PIP_OUTPUT=$("$VENV_DIR/bin/python" -m pip install --upgrade pip)

# Upgrade pip if needed
echo
echo "Upgrading pip"

if echo "$PIP_OUTPUT" | grep -q "Requirement already satisfied: pip"; then
    echo "Pip already up to date"
else
    echo "Pip version upgraded"
fi

REQ_FILE="$PROJECT_DIR/requirements.txt"

if [ ! -f "$REQ_FILE" ]; then
    echo "WARNING: requirements.txt not found"
fi

echo
echo "Installing dependencies..."
echo

"$VENV_DIR/bin/python" -m pip install -r "$REQ_FILE" 2>&1 | \
grep -E "Collecting|Installing|Successfully|Requirement" | \
while IFS= read -r line; do

    if [[ "$line" == Collecting* ]]; then
        echo "$line" | awk '{print $1, $2}'

    elif [[ "$line" == Requirement* ]]; then
        echo "$line" | awk '{print $1, $3, $4}'

    elif [[ "$line" == Installing* ]]; then
        echo
        echo "$line"

    else
        echo "$line"
    fi

done

echo
echo "================================"
echo "Setup Complete!"
echo "To activate run: "source $VENV_DIR"/bin/activate"
echo "================================"
echo

: << 'NOTES'

! command -v python3 > /dev/null
    ! = NOT
    command -v python3
        command = 
        -v =
        python3 =
    > /dev/null
        > =
        /dev/null = 

exit 1 = stops the script immediately

! python3 -m venv --help /dev/null 2>&1
    ! = NOT
    python3 -m venv = Tells python to create a virtual environment
    --help = Returns a help guide on left command
    /dev/null =
    2>&1
        2 =
        > =
        & =
        1 =

NOTES
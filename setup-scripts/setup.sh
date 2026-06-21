#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo
echo "Project Directory: $PROJECT_DIR"
echo "Script Directory: $SCRIPT_DIR"
echo
echo "Checking for Python Virtual Environment..."

# Check if .venv exists
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
echo "To activate run: "$VENV_DIR"/bin/activate"
echo "================================"
echo

: << 'NOTES'

NOTES
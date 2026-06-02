#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${1:-agent_learn}"
PYTHON_VERSION="${PYTHON_VERSION:-3.10}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS_FILE="$PROJECT_ROOT/cli-agent/requirements.txt"

if ! command -v conda >/dev/null 2>&1; then
  echo "Error: conda is not installed or not available in PATH." >&2
  exit 1
fi

if [ ! -f "$REQUIREMENTS_FILE" ]; then
  echo "Error: requirements file not found: $REQUIREMENTS_FILE" >&2
  exit 1
fi

echo "Project root: $PROJECT_ROOT"
echo "Conda env: $ENV_NAME"
echo "Python version: $PYTHON_VERSION"

if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  echo "Conda environment already exists: $ENV_NAME"
else
  echo "Creating conda environment: $ENV_NAME"
  conda create -y -n "$ENV_NAME" "python=$PYTHON_VERSION" pip
fi

echo "Installing Python dependencies..."
conda run -n "$ENV_NAME" python -m pip install --upgrade pip
conda run -n "$ENV_NAME" python -m pip install -r "$REQUIREMENTS_FILE"

echo
echo "Environment is ready."
echo "Activate it with:"
echo "  conda activate $ENV_NAME"
echo
echo "Before running the CLI agent, set your API key:"
echo "  export DEEPSEEK_API_KEY='your_deepseek_api_key'"
echo
echo "Run:"
echo "  python cli-agent/learn.py"

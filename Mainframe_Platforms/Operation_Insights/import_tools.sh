#!/usr/bin/env bash
# set -x
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "SCRIPT_DIR: ${SCRIPT_DIR}"

for python_tool in "${SCRIPT_DIR}/tools/"*; do
  # Skip if not a .py file
  if [[ "${python_tool}" != *.py ]]; then
    continue
  fi

  orchestrate tools import \
    -k python \
    -f "${python_tool}" \
    -r "${SCRIPT_DIR}/requirements.txt" \
    -p "${SCRIPT_DIR}/tools"
done

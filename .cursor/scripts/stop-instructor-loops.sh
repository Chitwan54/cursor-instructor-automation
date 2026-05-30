#!/usr/bin/env bash
# Stop launchd-managed instructor automation loops.
set -euo pipefail

STATE_DIR="${HOME}/Library/Application Support/instructor-automation"
INSTALL_DIR="${STATE_DIR}/scripts"

for name in daily sunday; do
  pidfile="${STATE_DIR}/${name}.pid"
  if [[ -f "${pidfile}" ]]; then
    pid="$(cat "${pidfile}")"
    if kill -0 "${pid}" 2>/dev/null; then
      kill "${pid}" && echo "Stopped ${name} (pid ${pid})"
    fi
    rm -f "${pidfile}"
  fi
done

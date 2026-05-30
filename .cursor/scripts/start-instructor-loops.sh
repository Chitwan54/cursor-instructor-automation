#!/usr/bin/env bash
# Start instructor automation loops (idempotent). Called by launchd on login.
set -euo pipefail

SCRIPT_ROOT="${HOME}/Library/Application Support/instructor-automation/scripts"
STATE_DIR="${HOME}/Library/Application Support/instructor-automation"
LOG_DIR="${HOME}/Library/Logs/instructor-automation"

mkdir -p "${STATE_DIR}" "${LOG_DIR}"

start_loop() {
  local name="$1"
  local script="$2"
  local pidfile="${STATE_DIR}/${name}.pid"

  if [[ -f "${pidfile}" ]]; then
    local old_pid
    old_pid="$(cat "${pidfile}")"
    if kill -0 "${old_pid}" 2>/dev/null; then
      echo "${name} already running (pid ${old_pid})"
      return 0
    fi
  fi

  nohup bash "${script}" >> "${LOG_DIR}/${name}.log" 2>&1 &
  echo "$!" > "${pidfile}"
  echo "Started ${name} (pid $!)"
}

start_loop "daily" "${SCRIPT_ROOT}/daily-slack-loop.sh"
start_loop "sunday" "${SCRIPT_ROOT}/sunday-feedback-loop.sh"

#!/usr/bin/env bash
# After agent completes, process one pending automation tick if queued.
set -euo pipefail

QUEUE="${HOME}/Library/Application Support/instructor-automation/pending-ticks.jsonl"

if [[ ! -s "${QUEUE}" ]]; then
  exit 0
fi

python3 - <<'PY'
import json
import os
import sys

queue = os.path.expanduser("~/Library/Application Support/instructor-automation/pending-ticks.jsonl")
with open(queue, encoding="utf-8") as f:
    lines = [ln.strip() for ln in f if ln.strip()]
if not lines:
    sys.exit(0)

record = json.loads(lines[0])
remaining = lines[1:]
with open(queue, "w", encoding="utf-8") as f:
    for line in remaining:
        f.write(line + "\n")

prompt = record["prompt"]
followup = (
    "PENDING AUTOMATION (scheduled tick: "
    + record.get("tick", "unknown")
    + "): "
    + prompt
)
print(json.dumps({"followup_message": followup}))
PY

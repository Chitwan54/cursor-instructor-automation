# Cursor Instructor Automation

Personal automation stack for Scaler (and other) instructor workflows — built on **Cursor skills**, **hooks**, **rules**, and **macOS launchd** timers. Originally set up for SST Data Analytics 101 (Batch 2029), but most pieces are reusable across courses.

## Architecture

```
macOS login
    └── launchd (com.chitwan.instructor-automation)
            └── start-instructor-loops.sh
                    ├── daily-slack-loop.sh      → 09:00 IST every day
                    └── sunday-feedback-loop.sh → 09:00 IST every Sunday
                            └── emit-automation-tick.sh
                                    ├── pending-ticks.jsonl (queue)
                                    └── macOS notification

Cursor (when open)
    └── .cursor/hooks.json → stop hook drains queue
            └── Agent runs skill → Slack MCP → DM to you
```

**Important:** Scheduled ticks queue work on your Mac even when Cursor is closed. The actual Slack work runs inside Cursor (via Slack MCP). Open Cursor in this project after a tick fires to process the queue.

---

## Automations

### 1. Daily Slack review

| | |
|---|---|
| **Skill** | `.cursor/skills/daily-slack-review/` |
| **Schedule** | Every day at **09:00 IST** |
| **Script** | `.cursor/scripts/daily-slack-loop.sh` |
| **What it does** | Scans `#ug-classroomops-instructor`, the course thread, Classroom Feedbacks DM, and DMs mentioning you. Produces a morning digest with action items, FYI, stale threads, and optional draft replies. Sends summary as a Slack DM. |
| **Manual trigger** | *"Run daily Slack review"* |

### 2. Sunday classroom feedback analysis

| | |
|---|---|
| **Skill** | `.cursor/skills/classroom-feedback-analysis/` |
| **Schedule** | Every **Sunday at 09:00 IST** |
| **Script** | `.cursor/scripts/sunday-feedback-loop.sh` |
| **Parser** | `.cursor/skills/classroom-feedback-analysis/scripts/parse_feedback.py` |
| **What it does** | Fetches Classroom Feedbacks bot reports from Slack, parses ratings and themes, appends to `data/classroom_ratings.csv`, computes week-on-week trends, and DMs you the full weekly report. |
| **Manual trigger** | *"Run classroom feedback analysis for SST DA 101"* |

### 3. Cohort assignment pipeline

| | |
|---|---|
| **Skill** | `.cursor/skills/cohort-assignment-pipeline/` |
| **Wraps** | `map-session-assignments` |
| **What it does** | End-to-end workflow: extract Scaler hire/test IDs from assignment tracker sheets, map them to syllabus sessions, build CSV/TSV outputs, and prepare internal syllabus column G paste lists. |
| **Config** | `config/cohorts/da101-2029.yaml` |
| **Manual trigger** | *"Run cohort assignment pipeline for DA101"* |

### 4. Map session assignments

| | |
|---|---|
| **Skill** | `.cursor/skills/map-session-assignments/` |
| **Scripts** | `extract_ids.py`, `build_mapping.py` |
| **What it does** | Lower-level skill for mapping problem/test-set IDs to syllabus session rows. Handles DAV trackers, DSML content sheets, and internal syllabus paste format. |
| **Output example** | `DA101_assignments_mapping.csv`, `paste_ids.tsv` |

### 5. Content reuse library

| | |
|---|---|
| **Skill** | `.cursor/skills/content-reuse-library/` |
| **Script** | `audit_colab_links.py` |
| **What it does** | Audits Colab links in the content library, flags broken/outdated links, and suggests quiz gaps for a cohort. |
| **Config** | `content/da101-2029/sessions.yaml` |
| **Manual trigger** | *"Audit content library for DA101"* |

### 6. Invoice maker

| | |
|---|---|
| **Skill** | `.cursor/skills/invoice-maker/` |
| **Status** | On hold — waiting for invoice template |

---

## Cursor primitives (how the pieces fit)

| Primitive | Location | Role |
|-----------|----------|------|
| **Rules** | `.cursor/rules/scaler-da101-instructor-context.mdc` | Always-on context: course links, contacts, automation index, pending-queue behavior |
| **Skills** | `.cursor/skills/*/SKILL.md` | Step-by-step playbooks the agent reads when a task matches |
| **Hooks** | `.cursor/hooks.json` + `.cursor/hooks/` | Event-driven scripts; `stop` hook drains one pending automation tick per agent completion (up to 3 chained) |
| **Config** | `config/instructor-automation.yaml` | Slack IDs, schedules, paths — edit per course/client |
| **launchd** | Installed via `install-instructor-automation.sh` | Restarts timer loops on every macOS login |

---

## Setup (after cloning)

### 1. Configure

Copy and edit `config/instructor-automation.yaml`:

- `instructor.slack_user_id` — your Slack user ID
- `slack.*` — channel/DM IDs for your workspace
- `courses.*.batch_filter` — feedback filter string
- `schedules.*.dm_user_id` — where automated DMs go

### 2. Cursor + Slack MCP

- Open this folder in Cursor
- Connect **Slack MCP** to your workspace (Scaler internal)
- Skills use Slack MCP for search, read, and send — no separate Slack API key needed

### 3. Install macOS timers (survives reboot)

```bash
bash .cursor/scripts/install-instructor-automation.sh
```

This copies scripts to `~/Library/Application Support/instructor-automation/scripts/`, registers LaunchAgent `com.chitwan.instructor-automation`, and starts both loops.

**Re-run after updating loop scripts in the repo.**

### 4. Useful commands

```bash
# Stop loops
bash .cursor/scripts/stop-instructor-loops.sh

# Logs
tail -f ~/Library/Logs/instructor-automation/daily.log
tail -f ~/Library/Logs/instructor-automation/sunday.log

# Pending queue (ticks waiting for Cursor)
cat ~/Library/Application\ Support/instructor-automation/pending-ticks.jsonl
```

---

## Repo layout

```
.cursor/
  hooks.json                 # Cursor stop hook → drain pending ticks
  hooks/                     # Hook scripts
  rules/                     # Always-on instructor context
  scripts/                   # launchd loop + install scripts
  skills/                    # Agent skill playbooks + Python helpers
config/
  instructor-automation.yaml # Master config
  cohorts/                   # Per-cohort assignment config
content/                     # Content library (partial)
data/
  classroom_ratings.csv      # Feedback ratings tracker
```

---

## Requirements

- macOS (for launchd login persistence)
- [Cursor](https://cursor.com) with Slack MCP connected
- Python 3 (for `parse_feedback.py` and assignment scripts)

---

## License

Private personal tooling. Scaler-internal links and IDs are for instructor use only; do not share outside the organization.

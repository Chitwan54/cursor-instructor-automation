---
name: daily-slack-review
description: >-
  Daily Slack digest for Scaler instructor ops — summarizes relevant channels/threads,
  extracts action items, and flags items needing reply. Use when the user asks for
  daily Slack review, morning digest, action items from Slack, or weekly ops catch-up.
---

# Daily Slack Review

Morning digest of Scaler Slack activity relevant to the instructor.

## Config

Read `config/instructor-automation.yaml` for channel IDs and course thread.

## Trigger phrases

- "Run daily Slack review"
- "What's pending in Slack?"
- "Morning digest"

**Recurring:** User can run `/loop 24h Run daily Slack review skill` in Cursor (see loop skill).

## Workflow

```
- [ ] 1. Read config (channels, course thread)
- [ ] 2. Scan priority sources (below)
- [ ] 3. Summarize + action items
- [ ] 4. Optional: DM draft replies
```

### Priority sources (Slack MCP)

| Source | Tool | What to look for |
|--------|------|------------------|
| `#ug-classroomops-instructor` | `slack_read_channel` / search | Cancellations, syllabus, assignments, ops flags |
| Course thread | `slack_read_thread` (thread_ts from config) | Rahul/academic ops requests, open items |
| Classroom Feedbacks DM | `slack_read_channel` on `D0A8QEGSL3Y` | New feedback since last review (don't full-analyze — use `classroom-feedback-analysis` on Sundays) |
| DMs mentioning you | `slack_search_public_and_private` query: `to:me after:yesterday` | Direct asks |

### Output format

```markdown
## Daily Slack Review — {date}

### Needs action (reply or task)
| Priority | Item | Source | Suggested action |
|----------|------|--------|------------------|

### FYI (no action)
- ...

### Stale / waiting on others
- ...

### Suggested replies (draft)
> ...
```

**Rules:**
- High priority: assignment/syllabus requests, student-facing blockers, same-day class changes
- Medium: attendance, content updates, feedback themes
- Low: FYI announcements
- Never send Slack messages without user approval unless explicitly asked

## Course-specific open items

Check instructor context rule (`.cursor/rules/scaler-da101-instructor-context.mdc`) for known action items and update if resolved.

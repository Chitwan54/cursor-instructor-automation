---
name: content-reuse-library
description: >-
  Audits course content library — Colab links, session materials, quiz gaps —
  and suggests cleanups, elaborations, and engagement improvements per session.
  Use when reviewing syllabus materials, Colab notebooks, content reuse across
  cohorts, or making sessions more engaging.
---

# Content Reuse Library

Maintain and audit reusable teaching assets per course.

## Library layout

```
content/
  {course-slug}/
    sessions.yaml      # session index (Colab links, status, quiz notes)
    colab-audit.md     # last audit report (generated)
data/
  classroom_ratings.csv  # cross-reference low-rated sessions
```

Seed: `content/da101-2029/sessions.yaml`

## Workflow

```
- [ ] 1. Export syllabus → extract Colab URLs (column D)
- [ ] 2. Run Colab link audit
- [ ] 3. Cross-reference feedback themes (pace, examples, assignments)
- [ ] 4. Per session: cleanup / elaboration / quiz suggestions
- [ ] 5. Update sessions.yaml status fields
```

### Step 1: Extract Colab links

```bash
curl -sL "https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx&gid={GID}" \
  -o /tmp/syllabus.xlsx

python .cursor/skills/content-reuse-library/scripts/audit_colab_links.py \
  --syllabus /tmp/syllabus.xlsx \
  --output content/da101-2029/sessions.yaml
```

### Step 2: Audit links

Script checks each Colab URL for HTTP 200 (public notebooks). Flags:
- Broken / permission-denied links
- Duplicate URLs across sessions
- Missing Colab for sessions that should have notebooks

### Step 3: Engagement review (per session)

For each session in `sessions.yaml`, produce:

| Check | Action |
|-------|--------|
| Colab link valid? | Fix or request access |
| Feedback cited "no assignments"? | Link to assignment mapping |
| Feedback cited "pace too slow" on basics? | Trim intro cells, add skip markers |
| Low rating + "examples" theme? | Add 2–3 in-class exercises |
| No in-class quiz listed? | Suggest 3–5 MCQ checks (see template below) |

### Quiz suggestion template

Per session, suggest:
- **2 recall MCQs** (definitions, syntax)
- **1 apply MCQ** (read code output)
- **1 discuss** (business POV from session title)

Do not write full quiz bank unless asked — list prompts only.

### Output format

```markdown
## Content Audit — {course} — {date}

### Broken / needs attention
| Session | Colab | Issue | Fix |

### Elaboration opportunities
| Session | Feedback signal | Suggestion |

### Quiz gaps (sessions without in-class checks)
| Session | Suggested quick checks |

### Reuse notes (for next cohort)
- ...
```

## Cross-course reuse

When starting a new cohort:
1. Copy `content/{old-slug}/` → `content/{new-slug}/`
2. Update sheet IDs in cohort config
3. Re-run audit

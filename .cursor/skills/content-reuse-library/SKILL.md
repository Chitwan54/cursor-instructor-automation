---
name: content-reuse-library
description: >-
  Audits course content library — Colab links, session materials, quiz gaps —
  writes a report, then asks which optional improvements to apply (quiz injection,
  Drive copies, syllabus updates). Use when reviewing syllabus materials, Colab
  notebooks, content reuse across cohorts, or making sessions more engaging.
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

**Two phases:** audit and report first; apply changes only after the user picks optional follow-ups.

```
Phase 1 — Audit (always)
- [ ] 1. Export syllabus → extract Colab URLs (column D)
- [ ] 2. Run Colab link audit → update sessions.yaml
- [ ] 3. Cross-reference feedback themes (pace, examples, assignments)
- [ ] 4. Write colab-audit.md (broken links, elaboration, quiz gaps, reuse notes)
- [ ] 5. Present summary to user

Phase 2 — Optional updates (user confirms; do not auto-apply)
- [ ] Ask which items from the menu below to run
- [ ] Execute only confirmed items; report what was skipped
```

### Ask before acting (required)

After Phase 1, **stop and ask** the user which optional updates they want. Use a short numbered menu; default is **report only**.

Example prompt:

> Content audit is done (`content/da101-2029/colab-audit.md`). Which optional updates should I run?
>
> 1. **In-class quizzes** — inject/revise opening + follow-up blocks in Colab notebooks (S3, S4, S9, S10)
> 2. **Quiz placement review** — fix Q4/follow-up anchors before students see case data (e.g. S9 Aerofit)
> 3. **Refresh Drive copies** — gist → Colab → Save a copy in Drive; update `colab_quiz_copy_links.csv`
> 4. **Update sessions.yaml** — quiz_notes, link status after changes
> 5. **Notebook trim / skip markers** — pace fixes from feedback (e.g. S3 repeat intro)
> 6. **Syllabus quiz column (E)** — draft prompts for internal sheet (list only unless paste access)
> 7. **Sharing / cleanup** — set Drive link sharing; delete superseded v1 copies
>
> Reply with numbers (e.g. `1, 3, 4`) or `none`.

**Rules:**
- Do **not** inject quizzes, edit notebooks, open browser/Drive, or overwrite YAML/CSV unless the user confirms.
- Quiz **suggestions** in the audit report stay as prompts until the user opts into (1) or (2).
- If the user flags a placement bug (e.g. case-specific Q4 at session start), propose a fix (generic opening Q4 + mid-session follow-up) and **confirm before editing**.
- After quiz content changes, remind user that Drive copies are stale until they confirm (3).

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

For each session in `sessions.yaml`, **document in the audit report** (do not implement unless user confirms Phase 2):

| Check | Suggested action (optional) |
|-------|----------------------------|
| Colab link valid? | Fix or request access |
| Feedback cited "no assignments"? | Link to assignment mapping |
| Feedback cited "pace too slow" on basics? | Trim intro cells, add skip markers |
| Low rating + "examples" theme? | Add 2–3 in-class exercises |
| No in-class quiz listed? | Suggest 3–5 MCQ checks (see template below) |
| Quiz already in notebook? | Note placement in `quiz_notes`; flag stale Drive copy |

### Quiz suggestion template

Per session, suggest:
- **2 recall MCQs** (definitions, syntax)
- **1 apply MCQ** (read code output)
- **1 discuss** (business POV from session title)

Do not write full quiz bank unless asked — list prompts only in the audit report.

### In-class quiz injection (Colab) — optional Phase 2

Run only when user confirms menu item **1** and/or **2**.

Script: `.cursor/skills/content-reuse-library/scripts/inject_colab_quizzes.py`

**Before editing:** read the target notebook structure; confirm opening vs follow-up placement with user if case-specific content is involved.

**Opening block** (6 cells, marker `<!-- da101-inclass-quiz -->`):
- Header → Q1 recall → Q2 recall → Q3 apply (code) → Q4 discuss → instructor key
- Place at **session start** (prepend) or immediately after the `## Content` outline (S4)
- ~5 minutes

**Follow-up block** (3 cells, marker `<!-- da101-inclass-quiz-followup -->`):
- Header → discuss prompt → instructor key
- Insert **after students have the case-study context** (anchor cell in notebook)
- ~2–3 minutes

**End-to-end when user confirms quiz + Drive refresh:**

```
1. Edit quiz content in inject_colab_quizzes.py (if needed)
2. python .cursor/skills/content-reuse-library/scripts/inject_colab_quizzes.py
3. gh gist create (or update) → open in Colab → File → Save a copy in Drive → rename
4. Update content/{slug}/colab_quiz_copy_links.csv
5. Update sessions.yaml quiz_notes (remove "needs refresh"; add quiz copy Drive ID)
6. Optionally delete superseded Drive copies (list IDs; confirm with user)
```

Drive copies: view-only syllabus originals stay unchanged; instructor uses editable copies in `colab_quiz_copy_links.csv`.

#### Placement rules (critical)

| Rule | Why |
|------|-----|
| Opening Q4 must not name datasets/segments students have not seen yet | Avoid Aerofit-segment questions before EDA |
| Opening Q3/Q4 may use **hypothetical numbers in the prompt** | CI / business decisions without loading data first (S9 Q3, S10 Q4) |
| Case-specific discuss questions → **follow-up block** anchored mid-notebook | S9 variance-by-segment after categorical analysis |
| Match the **actual notebook dataset**, not syllabus title alone | S3/S4 Colabs use IMDB + drug experiment data, not a generic “Entertainment” sheet |
| Re-run inject script after edits; it strips old blocks via markers + orphan Q1 cells | Prevents duplicate quiz cells in Drive copies |

#### Current session layout

| Session | Opening placement | Follow-up anchor |
|---------|-------------------|------------------|
| S3 | Prepend | After “Here we have two CSV files” — IMDB merge checks |
| S4 | After `## Content` | After drug-data `pivot_table` example |
| S9 | Prepend | Before multivariate scatterplot section — Aerofit usage variance |
| S10 | Prepend | None (Q4 uses hypothetical $45 target + CI in prompt) |

Regenerate local notebooks (after user confirms quiz work):

```bash
python .cursor/skills/content-reuse-library/scripts/inject_colab_quizzes.py
```

## Audit report template

Write to `content/{course-slug}/colab-audit.md`:

```markdown
## Content Audit — {course} — {date}

### Summary
| Metric | Count |

### Broken / needs attention
| Session | Colab | Issue | Fix |

### Elaboration opportunities
| Session | Feedback signal | Suggestion |

### Quiz gaps / quiz status
| Session | Status | Suggested quick checks or notes |

### Optional follow-ups (confirm with user)
- [ ] Inject/revise in-class quizzes (sessions: …)
- [ ] Refresh Drive copies (`colab_quiz_copy_links.csv`)
- [ ] Trim notebooks / skip markers
- [ ] Draft syllabus quiz column (E)
- [ ] Drive sharing / delete stale copies

### Reuse notes (for next cohort)
- ...
```

After saving the report, present the Phase 2 menu (see **Ask before acting**).

## Cross-course reuse

When starting a new cohort:
1. Copy `content/{old-slug}/` → `content/{new-slug}/`
2. Update sheet IDs in cohort config
3. Re-run audit

---
name: map-session-assignments
description: >-
  Maps Scaler hire/test problem IDs from assignment tracker sheets to syllabus
  sessions. Extracts IDs from Google Sheets/Docs hyperlinks, builds session→ID
  tables, and optionally pastes into internal syllabus sheets. Use when the user
  asks to map assignments to sessions, populate Links to Assignments, build
  assignment mapping tables, or sync syllabus with assignment trackers for any
  course (Data Analytics, ML, DL, etc.).
---

# Map Session Assignments

Map problem IDs from **assignment source sheet(s)** to **syllabus session rows**.

## Inputs (required)

| Input | What to collect |
|-------|-----------------|
| **Syllabus sheet** | Google Sheet URL or exported `.xlsx`/`.csv`. Must have session numbers and titles. |
| **Assignment sheet(s)** | One or more trackers (Google Sheet, Doc, or `.xlsx`). May span multiple files/tabs. |

## Clarifying questions (ask before finalizing)

Ask only what's ambiguous for this run:

1. **Scope** — Which session range? Skip sessions already covered?
2. **Include homework?** — Default: yes (assignments + homework combined in one ID list).
3. **Exclusions** — Skip red/"not in use"/"not covered in script" rows?
4. **Split rules** — When one assignment tab covers multiple syllabus sessions, confirm split (e.g. Pandas Lec1–3 → Session 3, Lec4–5 → Session 4).
5. **Output** — Table only, CSV file, Slack DM, or paste into internal syllabus?
6. **Syllabus column** — Default: **G (`Links to Assigments`)**. Leave other columns untouched.

## Workflow

```
Task Progress:
- [ ] 1. Parse syllabus sessions
- [ ] 2. Download & extract problem IDs from assignment sources
- [ ] 3. Propose tab/lecture → session mapping (show counts per session)
- [ ] 4. Get user confirmation on ambiguous splits
- [ ] 5. Build final table + CSV
- [ ] 6. (Optional) Paste into internal syllabus sheet
```

### Step 1: Parse syllabus

Export syllabus as xlsx when possible:

```
https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx&gid={GID}
```

Read columns (names vary slightly):

| Column | Typical header |
|--------|----------------|
| A | Session Number |
| B | Session Title |
| F | Assignments (problem names — often leave as-is) |
| G | Links to Assigments (target for ID lists) |
| H | Additional Problems (Homework) |

Build a session list: `{number, title, row_index}`.

### Step 2: Extract problem IDs

**Preferred method** — export assignment Google Sheets as xlsx (preserves hyperlinks):

```
https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx&gid={GID}
```

Run the extraction script on each source file:

```bash
python .cursor/skills/map-session-assignments/scripts/extract_ids.py \
  --input ~/Downloads/assignment-tracker.xlsx \
  --output /tmp/extracted.json
```

For Google Docs (e.g. FE assessments), export as `.docx` and pass `--docx`.

**ID URL patterns:**

| Pattern | ID type | Example |
|---------|---------|---------|
| `/hire/test/problem/{id}/` | Problem ID | `26957` |
| `/hire/test/{id}/` | Test-set ID | `477525` |

Both are valid output IDs. Flag test-set IDs in notes when no individual problem breakdown exists.

**Column conventions in Scaler trackers** (varies by tab):

- NumPy/Pandas: C = Assignment, E = Homework
- Data Viz: C = Assignment, D = Homework
- DSML Content Sheet: columns 9–10 = Assignment / Homework per topic row

**Exclusions:** Skip cells/rows marked red, "not in use", or "not covered in script".

### Step 3: Propose mapping

Match assignment source sections to syllabus sessions by:

1. **Topic alignment** — lecture names ↔ session titles (NumPy → "Data Analytics Using Numpy")
2. **Explicit lecture splits** — when one tab spans multiple sessions, split by lecture number
3. **One source → one session** — when granularity matches (whole NumPy tab → Session 2)

Present a **draft mapping table** before finalizing:

| Syllabus Session | Source | Lectures/Tabs | # IDs |
|------------------|--------|---------------|-------|

Highlight ambiguous cases and wait for user confirmation.

### Step 4: Build output

**Default table format** (3 columns — no Problem Name unless requested):

```
| Session Number | Session Details | Problem ID List |
```

Also write a CSV: `{course}_assignments_mapping.csv`

ID list format: comma-separated, ascending within each session, deduplicated.

### Step 5: Paste into internal syllabus (optional)

Target cell range: **G{first_session_row}:G{last_session_row}**

**Pre-check:** User must have **Editor** access (not View only).

1. Build `paste_ids.tsv` — one ID list per line, session order
2. Select **G3** (or first session row), paste TSV (fills down)
3. Do **not** modify Session 1, column F, or other columns unless asked

**Fallback if browser paste fails:** Patch column G in exported xlsx with openpyxl, provide file for manual import.

## Accessing Google Sheets

If direct fetch fails (auth required):

1. Ask user to make sheet link-viewable, **or**
2. Use Cursor browser (user logged into Google), **or**
3. User exports and attaches `.xlsx`

Never sign into Google on the user's behalf.

## Deliverables checklist

- [ ] Draft mapping with per-session ID counts (for user LGTM)
- [ ] Final markdown table
- [ ] CSV file saved locally
- [ ] Slack DM if requested (markdown table, not CSV attachment — Slack MCP can't upload files)
- [ ] Syllabus paste or blocker note (e.g. view-only access)

## Additional resources

- Sheet formats, edge cases, DA101 walkthrough: [reference.md](reference.md)
- Worked example: [examples.md](examples.md)

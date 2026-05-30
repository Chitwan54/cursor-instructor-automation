# Reference: Assignment Mapping

## Scaler URL patterns

```
https://www.scaler.com/hire/test/problem/{PROBLEM_ID}/
https://www.scaler.com/hire/test/{TEST_SET_ID}/
```

- **Problem IDs** — individual coding problems; preferred when available.
- **Test-set IDs** — assignment bundles (common in DSML Content Sheet for LR/Logistic Regression). Include as-is; note in output that they are test-set IDs.

## Syllabus sheet structure (Scaler internal)

Typical internal syllabus columns:

| Col | Header | Role |
|-----|--------|------|
| A | Session Number | Match key |
| B | Session Title | Display |
| C | Topics/Flow | Leave untouched |
| D | Class Material | Leave untouched |
| E | Count of In-class Quizzes | Leave untouched |
| F | Assignments | Problem names (optional; may pre-exist) |
| G | Links to Assigments | **Paste target for ID lists** |
| H | Additional Problems (Homework) | Usually empty when IDs combined in G |
| J+ | Evaluation, dates, weightage | Leave untouched |

Row offset: Session N is typically row N+1 (Session 2 → row 3).

## Assignment tracker layouts

### Pattern A: Lecture-grouped assessments (Python/DAV trackers)

Tabs like `NumPy assessments`, `Pandas assessments`, `Data Viz assessments`.

- Col A: Lecture number
- Col B: Topic name
- Cols C–E: Assignment / Homework cells with hyperlinks
- Group by lecture, then map lecture groups → syllabus sessions

### Pattern B: Lecture-numbered grid (DAV-2 stats)

Tab `Assessments` with lectures 1–11 in col A/B, problems in cols C–Z.

- Map multiple lectures → one syllabus session when syllabus compresses topics
- Example: Lectures 1–5 → Session 9 (Aerofit), Lectures 6+8+10+11 → Session 7 (Sachin)

### Pattern C: Topic rows (DSML Content Sheet)

Tab `Intro to ML and NN` — one row per ML topic.

- Cols I–J (9–10): Assignment / Homework hyperlinks
- Often `/hire/test/{id}/` not `/problem/{id}/`

### Pattern D: Google Doc sections (Feature Engineering)

Doc with sections `Feature Engineering - 1`, `Feature Engineering - 2`.

- Export as `.docx`, parse hyperlinks per section
- Combine sections when syllabus has one FE session

## Mapping heuristics

1. **Name match** — fuzzy match session title ↔ lecture/topic name
2. **Lecture range split** — when user confirms (Pandas Lec1–3 vs Lec4–5)
3. **Move problems between sessions** — user may relocate specific IDs (e.g. subplots → Session 6)
4. **Skip sessions** — no coding problems (RCA, Guess Estimates) → mark N/A
5. **Prior semester coverage** — user may say leave Session 1 as-is

## Exclusion rules

Skip problems when source row/cell indicates:

- Red background / flagged in sheet
- Text: "not in use", "not covered in script", "deprecated"

## Google access methods

| Method | When |
|--------|------|
| `export?format=xlsx&gid={GID}` | Sheet is link-accessible (viewer OK) |
| Cursor browser + user Google login | Sheet requires auth |
| User attaches export | Browser auth unavailable |

## Pasting into Google Sheets

**Blockers:**

- View-only access → cannot paste; ask for Editor role
- Smart-chip dialog on hyperlink cells → dismiss with Escape before paste
- Cursor browser clipboard paste may fail → use formula bar F2 edit or openpyxl patch + manual import

**Paste technique:**

1. Create TSV with one ID list per line (sessions in order)
2. Select G{first_row}, paste → fills down
3. Verify via re-export

## Output files

| File | Purpose |
|------|---------|
| `{course}_assignments_mapping.csv` | Full mapping archive |
| `paste_ids.tsv` | One line per session for column G paste |
| `session_map.json` | Machine-readable mapping config for `build_mapping.py` |

## session_map.json schema

```json
{
  "7": {
    "title": "Probability Distributions (Sachin)",
    "sources": [
      {"tab": "Assessments", "sections": ["6 - Probability Distributions 1", "8 - ..."]}
    ]
  },
  "11": {
    "title": "Linear Regression",
    "ids": ["477525", "477526", "477530", "477531", "477533", "785633", "785634"]
  }
}
```

Use explicit `"ids"` when source uses test-set URLs or manual curation is needed.

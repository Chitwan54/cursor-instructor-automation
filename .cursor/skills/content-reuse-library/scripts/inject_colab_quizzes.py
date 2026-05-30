#!/usr/bin/env python3
"""Inject in-class quiz cells into DA101 Colab notebooks."""
from __future__ import annotations

import json
from pathlib import Path

QUIZ_MARKER = "<!-- da101-inclass-quiz -->"
FOLLOWUP_MARKER = "<!-- da101-inclass-quiz-followup -->"


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": [text]}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": [text],
        "outputs": [],
        "execution_count": None,
    }


def quiz_block(session: int, title: str, recall: list[str], apply_src: str, discuss: str) -> list[dict]:
    header = md(
        f"{QUIZ_MARKER}\n"
        f"# In-class Quiz — Session {session}: {title}\n\n"
        f"*~5 minutes. Discuss answers aloud before expanding the instructor key.*\n"
    )
    recall_cells = [md(q) for q in recall]
    apply_cell = code(apply_src)
    discuss_cell = md(f"**Q4 (Discuss):** {discuss}\n")
    key = md(
        "---\n"
        "### Instructor answer key\n"
        "- See discussion above / cell output for apply question.\n\n"
        "*Remove or collapse this section before sharing if you prefer live-only discussion.*\n"
    )
    return [header, *recall_cells, apply_cell, discuss_cell, key]


def followup_block(session: int, label: str, discuss: str, key: str = "") -> list[dict]:
    header = md(
        f"{FOLLOWUP_MARKER}\n"
        f"## In-class Check-in — Session {session}: {label}\n\n"
        f"*~2–3 minutes. Pause here — students should have the case-study context above.*\n"
    )
    discuss_cell = md(f"**Discuss:** {discuss}\n")
    key_text = key or "See discussion."
    key_cell = md(f"---\n### Instructor answer key\n- {key_text}\n")
    return [header, discuss_cell, key_cell]


OPENING_QUIZZES = {
    3: quiz_block(
        3,
        "Pandas — Data Loading & Cleaning",
        [
            "**Q1 (Recall):** When should you use `pd.read_csv()` vs `pd.read_excel()`?\n\n"
            "- A) Always CSV for larger files\n"
            "- B) CSV for plain-text exports; Excel when sheets or formatting matter\n"
            "- C) Excel is always safer\n\n"
            "<details><summary>Key</summary>B — match the file format and whether you need sheet selection.</details>",
            "**Q2 (Recall):** What does `df.isna().sum()` tell you?\n\n"
            "<details><summary>Key</summary>Missing-value count **per column** — first step in a data-quality audit.</details>",
        ],
        """# Q3 (Apply) — missing values
import pandas as pd

dirty = pd.DataFrame({"title": ["A", None, "C"], "rating": [4.5, 3.0, None]})
print("Missing per column:\\n", dirty.isna().sum())
print("\\nAfter dropna (rows with ANY null):\\n", dirty.dropna())
print("\\nAfter fillna on rating only:\\n", dirty.assign(rating=dirty["rating"].fillna(dirty["rating"].median())))
# Which approach you pick depends on whether missingness is structural or imputable.
""",
        "Why should we inspect missing values and dtypes **before** plotting or aggregating — even when a dataset looks fine at first glance?",
    ),
    4: quiz_block(
        4,
        "Pandas — Transformation & Cleaning",
        [
            "**Q1 (Recall):** What is the main purpose of `pd.melt()`?\n\n"
            "<details><summary>Key</summary>Convert wide data to long/tidy format — one row per observation.</details>",
            "**Q2 (Recall):** How is `pd.pivot()` different from `pd.pivot_table()`?\n\n"
            "<details><summary>Key</summary>`pivot` needs unique index/column pairs; "
            "`pivot_table` aggregates (handles duplicates via aggfunc).</details>",
        ],
        """# Q3 (Apply) — pivot vs melt
import pandas as pd

wide = pd.DataFrame({"region": ["North", "South"], "Q1": [10, 20], "Q2": [15, 25]})
long = wide.melt(id_vars="region", var_name="quarter", value_name="sales")
print("Melted (long format):\\n", long)
print("\\nPivoted back:\\n", long.pivot(index="region", columns="quarter", values="sales"))
""",
        "Name **one analytics question** that is easier to answer after reshaping wide data into long (tidy) format.",
    ),
    9: quiz_block(
        9,
        "Descriptive Statistics & Probability — Aerofit",
        [
            "**Q1 (Recall):** For a skewed revenue distribution, which is more representative — mean or median? Why?\n\n"
            "<details><summary>Key</summary>Median — less pulled by extreme outliers.</details>",
            "**Q2 (Recall):** In plain language, what does a **p-value** help us judge?\n\n"
            "<details><summary>Key</summary>How surprising the observed result would be if there were truly no effect (null hypothesis).</details>",
        ],
        """# Q3 (Apply) — read a confidence interval
import numpy as np

np.random.seed(42)
sample = np.random.normal(loc=500, scale=80, size=30)  # hypothetical monthly spend ($)
mean = sample.mean()
se = sample.std(ddof=1) / np.sqrt(len(sample))
ci_low, ci_high = mean - 1.96 * se, mean + 1.96 * se
print(f"Sample mean spend: ${mean:.0f}")
print(f"Approx 95% CI: [${ci_low:.0f}, ${ci_high:.0f}]")
print("If target spend is $650 and CI upper bound is below $650, what would you conclude?")
""",
        "Based on the CI above, would you tell leadership that average spend meets the **$650** target? "
        "What does the interval tell you — and what does it **not** tell you?",
    ),
    10: quiz_block(
        10,
        "CLT & Confidence Intervals — Walmart",
        [
            "**Q1 (Recall):** State the Central Limit Theorem in one sentence.\n\n"
            "<details><summary>Key</summary>Sample means approach a normal distribution as sample size grows, "
            "regardless of population shape (under common conditions).</details>",
            "**Q2 (Recall):** What does a **95% confidence interval** for a mean represent?\n\n"
            "<details><summary>Key</summary>A range of plausible values for the population mean; "
            "95% of similarly constructed intervals would contain the true mean.</details>",
        ],
        """# Q3 (Apply) — sample size and CI width
import numpy as np

def ci_width(n, sigma=120):
    se = sigma / np.sqrt(n)
    return 2 * 1.96 * se  # approximate 95% CI width

for n in [25, 100, 400]:
    print(f"n={n:3d} -> CI width ≈ {ci_width(n):.1f}")
print("\\nWhat happens to CI width when n quadruples?")
""",
        "If a store's target average purchase is **$45** and your 95% CI is **[$38, $42]**, "
        "what would you recommend to leadership?",
    ),
}

FOLLOWUP_QUIZZES: dict[int, list[tuple[str, list[dict], str]]] = {
    3: [
        (
            "Here we have two CSV files",
            followup_block(
                3,
                "IMDB data loaded",
                "Before merging `movies` and `directors`, what **two checks** would you run on each table?",
                "Row counts, dtypes, missing values, key uniqueness (e.g. `director_name`), and whether join keys align.",
            ),
            "after",
        ),
    ],
    4: [
        (
            "pd.pivot_table(data_tidy, index='Drug_Name', columns='Date', values=['Temperature', 'Pressure']",
            followup_block(
                4,
                "After melt & pivot",
                "For the drug experiment data above, what insight is easier to answer with `pivot_table` "
                "and an aggregation (e.g. mean) than with the raw wide table?",
                "Day-wise or drug-wise average temperature/pressure — duplicates require aggregation via `pivot_table`.",
            ),
            "after",
        ),
    ],
    9: [
        (
            "#### Multivariate Analysis using Scatterplots",
            followup_block(
                9,
                "Aerofit — usage by segment",
                "Which Aerofit customer segment likely has the **highest variance** in weekly usage — "
                "and why does that matter for marketing?",
                "Premium / high-usage segments (e.g. KP781 buyers) often show wider usage spread; "
                "high variance means average-only campaigns miss inconsistent users.",
            ),
            "before",
        ),
    ],
}


def has_marker(cells: list[dict], marker: str) -> bool:
    return any(marker in "".join(c.get("source", [])) for c in cells)


def _skip_through_instructor_key(cells: list[dict], i: int) -> int:
    while i < len(cells):
        if "### Instructor answer key" in "".join(cells[i].get("source", [])):
            return i + 1
        i += 1
    return i


def strip_quiz_cells(cells: list[dict]) -> list[dict]:
    """Remove full quiz blocks (header through instructor key) and orphan quiz fragments."""
    out: list[dict] = []
    i = 0
    while i < len(cells):
        src = "".join(cells[i].get("source", []))
        if QUIZ_MARKER in src or FOLLOWUP_MARKER in src:
            i = _skip_through_instructor_key(cells, i + 1)
            continue
        if src.startswith("**Q1 (Recall):**"):
            i = _skip_through_instructor_key(cells, i + 1)
            continue
        out.append(cells[i])
        i += 1
    return out


def find_cell_index(cells: list[dict], text_substr: str) -> int:
    for i, c in enumerate(cells):
        if text_substr in "".join(c.get("source", [])):
            return i
    raise ValueError(f"Anchor not found: {text_substr!r}")


def inject_opening(cells: list[dict], session: int, *, prepend: bool, after_anchor: str | None) -> list[dict]:
    block = OPENING_QUIZZES[session]
    if prepend:
        return block + cells
    if after_anchor is None:
        raise ValueError("after_anchor required when prepend=False")
    idx = find_cell_index(cells, after_anchor)
    return cells[: idx + 1] + block + cells[idx + 1 :]


def inject_followups(cells: list[dict], session: int) -> list[dict]:
    for anchor, block, placement in FOLLOWUP_QUIZZES.get(session, []):
        idx = find_cell_index(cells, anchor)
        insert_at = idx if placement == "before" else idx + 1
        cells = cells[:insert_at] + block + cells[insert_at:]
    return cells


def build_notebook(cells: list[dict], session: int, *, prepend: bool, after_anchor: str | None) -> list[dict]:
    cells = strip_quiz_cells(cells)
    cells = inject_opening(cells, session, prepend=prepend, after_anchor=after_anchor)
    cells = inject_followups(cells, session)
    return cells


def main() -> None:
    base = Path(__file__).resolve().parents[4] / "content" / "da101-2029" / "notebooks"
    base.mkdir(parents=True, exist_ok=True)

    jobs = [
        (3, base / "session3_with_quizzes.ipynb", base / "session3_with_quizzes.ipynb", True, None),
        (4, base / "session4_with_quizzes.ipynb", base / "session4_with_quizzes.ipynb", False, "## Content"),
        (9, base / "session9_with_quizzes.ipynb", base / "session9_with_quizzes.ipynb", True, None),
        (10, base / "session10_with_quizzes.ipynb", base / "session10_with_quizzes.ipynb", True, None),
    ]

    for session, src, out, prepend, anchor in jobs:
        if not src.exists():
            print(f"skip S{session}: missing {src.name}")
            continue
        nb = json.loads(src.read_text())
        nb["cells"] = build_notebook(nb["cells"], session, prepend=prepend, after_anchor=anchor)
        out.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
        opening = has_marker(nb["cells"], QUIZ_MARKER)
        followups = sum(1 for c in nb["cells"] if FOLLOWUP_MARKER in "".join(c.get("source", [])))
        print(f"Wrote {out.name} ({len(nb['cells'])} cells, followup blocks={followups})")

    for session in (3, 9):
        patch = {
            "nbformat": 4,
            "nbformat_minor": 0,
            "metadata": {"colab": {"provenance": []}, "kernelspec": {"name": "python3", "display_name": "Python 3"}},
            "cells": OPENING_QUIZZES[session]
            + [
                md(
                    "---\n"
                    f"**Next step:** Copy the cells above into the top of the Session {session} Colab, "
                    "or upload this file and merge manually.\n"
                )
            ],
        }
        out = base / f"session{session}_quiz_cells_only.ipynb"
        out.write_text(json.dumps(patch, indent=1, ensure_ascii=False) + "\n")
        print(f"Wrote {out.name} (opening quiz only — paste into live Colab)")


if __name__ == "__main__":
    main()

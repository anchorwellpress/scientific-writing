# Recognition Capture Log

<!--
HOW TO USE:
  - Paste this file (or its contents) at the top of any new scientific-writing project
  - Keep it open in a side window while drafting, or paste as HTML comment at top of manuscript
  - When a trigger fires during writing, add one row to the table below
  - At session end, fill in the Session Summary block
  - For longer projects, migrate captures into the full citation_log.md Recognition Capture Log section

Recognition Capture is the upstream discipline: catch fabrication at the moment of generation,
before it enters prose. The verification gates downstream catch what slipped through.
The goal is many captures and zero Gate 2 failures — that pattern means recognition is fully engaged.
-->

**Project:** [name]
**Session date:** [date]
**Register:** [peer-reviewed / long-form / brief communication / essay]

---

## The Six Recognition Triggers (Keep Visible While Writing)

When any of these is about to happen, STOP before completing the sentence:

| # | Trigger | What it sounds like in your own head |
|---|---|---|
| 1 | About to write a PMID, DOI, or PMC ID | "I think the PMID is..." |
| 2 | About to write a specific number or effect size | "...reduced by 22%..." "...n=2,847..." |
| 3 | About to describe a specific study | "A 2018 RCT showed..." "In a recent journal article..." |
| 4 | About to attribute a position to a named author | "[Senior author] and colleagues..." "[Frequently-cited researcher] has argued..." |
| 5 | About to write a date or temporal anchor | "In 2021..." "Since 2009..." |
| 6 | About to write "research has shown" / "studies suggest" | citation-implying language without ready citations |

## The Three Resolutions

When a trigger fires, pick one:

- **Retrieve** — Search PubMed (via `PubMed:search_articles` or `verify_citation.py`) for the real source, verify it matches the claim, then write the sentence with verified content.
- **Placeholder** — Write `[UNVERIFIED: brief description of what's needed]`. Resolve before the next paragraph.
- **Rewrite** — Reformulate the sentence to not require the unverified element (e.g., qualitative language instead of a specific number).

---

## Capture Log (Add Rows As Triggers Fire)

| Time | Section | Trigger # | What was about to be written | Resolution | Outcome |
|---|---|---|---|---|---|
| 14:32 | Background | 1 | "...PA burden [Cite: PMID:29346583]" — was about to use PMID from memory | Retrieve | Searched PubMed; retrieved PMID 35296630 (Shah ED et al. AJG 2022); content verified |
| 14:38 | Background | 2 | "About two-thirds of physicians..." — was generating a plausible-sounding fraction | Retrieve | Abstract says "Greater than 50%"; used verified phrasing |
| 14:45 | Background | 3+4 | "Hoffman and colleagues developed the CITE framework..." | Placeholder | `[UNVERIFIED: CITE framework attribution]` pending PubMed search for actual framework paper |
|   |   |   |   |   |   |

---

## Session Summary (Fill At Session End)

**Total captures this session:** [N]
**Total citations finalized this session:** [M]
**Recognition-to-citation ratio:** [N/M]
**Gate 2 failures this session:** [count]

### Pattern Detection

- **Most frequent trigger:** [e.g., Trigger 1 (PMIDs)]
- **Subfield clustering:** [e.g., captures concentrated in prior authorization]
- **Author-name clustering:** [e.g., [senior author name] triggered 3 captures]
- **Sentence-construction clustering:** [e.g., "Recent work has shown..." triggered 2 captures]
- **Time-of-session clustering:** [early / mid / late session — discipline drops late]

### What to Watch For Next Session

- [Specific pattern noticed this session that warrants extra vigilance]
- [Subfield or author where verification needs to slow down]
- [Sentence construction to avoid or to verify on first appearance]

---

## Trend Across Sessions (Append Each Session)

| Date | Section worked | Captures | Citations finalized | Gate 2 failures | Note |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

**Target pattern:** Many captures, zero Gate 2 failures. That combination means recognition is fully engaged and the manuscript is clean before it reaches the gates.

**Warning pattern:** Zero captures with Gate 2 failures. Recognition is not running; verification load fell on the gates instead.

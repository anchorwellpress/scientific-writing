# Citation Log — [Project Name]

**Project:** [e.g., your manuscript title or working name]
**Target venue:** [e.g., target journal name, book series, magazine, blog platform]
**Register:** [peer-reviewed / long-form / brief communication]
**Word-count target:** [e.g., 3,500 for a research article, 1,500 for brief communication]
**Started:** [date]
**Last audit:** [date — run audit_manuscript.py and update]
**Manuscript version:** [v1 / v2 / revision-round-1 / etc.]

---

## AI Use Disclosure (for submission)

Track AI use for the journal's required disclosure statement. Update each session.

**System used:** [e.g., Claude (Anthropic), version Opus 4.7]

**AI was used for:**
- [ ] Literature search and triage
- [ ] Drafting prose
- [ ] Editing and revision
- [ ] Citation verification (Gate 2)
- [ ] Citation fact-match review (Gate 4)
- [ ] Statistical analysis
- [ ] Code generation
- [ ] Figure or table generation
- [ ] None

**Sections AI-assisted:**
- [List sections with degree of assistance: e.g., "Introduction drafted with AI assistance, Methods authored without AI, Results tables generated with AI assistance and manually verified"]

**Verification:** All AI-generated citations passed Gate 2 (existence) and Gate 4 (fact match) per the scientific-writing skill protocol. Author retains full responsibility for content accuracy.

**Draft disclosure statement for submission:**
> "The authors used [AI system + version] during [specific tasks] in the preparation of this manuscript. All AI-assisted content was verified by the authors. Specifically, [list verification: e.g., all citations were checked against PubMed and Crossref records, and abstracts were reviewed to confirm fact-match for every load-bearing claim]. The authors retain full responsibility for the integrity and accuracy of all content."

---

## How to Use This Log

Every citation added to the manuscript appears here. The log is the source of truth.

- Add a row when a citation is first added to the draft.
- Run `verify_citation.py` and record the Gate 2 verdict.
- Read the abstract; walk Gate 4 (Q1–Q4) and record the result.
- A citation with Gate 2 PASS but no Gate 4 result is NOT cleared for submission.
- If a citation is removed from the draft, mark it RETIRED (don't delete — keeps history).
- For non-indexed sources, use the non-indexed verification protocol and log accordingly.

A citation in the draft that isn't in this log is suspect. A citation in the log without Gate 4 completed is not cleared.

---

## Indexed Citations (PubMed/Crossref)

| # | PMID/DOI | First Author | Year | Brief Title | Status | Claim Supported | Path A Gate 2 (date) | Path A Gate 4 Q1-Q4 (date, abstract/full-text) | Path B (date, verdict) | Final | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PMID:[xxxxxxxx] | [Last F] | [year] | [brief title] | indexed | "[claim being supported]" | PASS ([date]) | PASS all Q1-Q4 ([date], full-text) | PASS ([date], MCP) | CLEARED | Both paths agree |
|   |   |   |   |   |   |   |   |   |   |   |   |

---

## Final Iterative Pass Log

The Final Iterative Pass runs Path B (PubMed MCP connector) against every citation after drafting is complete and before formatting. A manuscript without a completed pass is not cleared for submission.

**Pass date:** [date]
**Total citations re-verified:** [N]
**Both paths PASS (cleared):** [N]
**Disagreements resolved:** [N]
**Citations replaced as a result:** [N]
**Full-text Gate 4 reviews performed:** [N]

### Disagreement Resolution Log

| Citation | Path A | Path B | Resolution | Action Taken |
|---|---|---|---|---|
| [PMID or ref] | PASS | FAIL | Pattern 4 — manual verification confirmed citation is real but stale PubMed cache caused MCP miss | Cleared after manual PubMed.gov search |
| [PMID or ref] | FAIL | PASS | Pattern 3 — Path A author-list discriminator caught wrong author list in manuscript; corrected | Manuscript citation corrected |

---

## Recognition Capture Log

Every time a recognition trigger fired during writing and a fabrication was caught before it entered prose. The log is diagnostic — patterns reveal which subfields, authors, and sentence constructions trigger captures most often.

| Date | Session | Trigger | What was about to be written | Resolution | Notes |
|---|---|---|---|---|---|
| 2026-05-15 | Drafting Background | Trigger 1 (PMID) | "...prior authorization burden [Cite: PMID:29346583]" — was about to use 29346583 from memory | Searched PubMed; actual paper at that PMID is unrelated. Replaced with `[UNVERIFIED: prior auth burden]` | Class 4 caught at recognition stage |
| 2026-05-15 | Drafting Methods | Trigger 3 (study description) | "A 2018 randomized trial demonstrated..." | Rewrote without specific study attribution; claim doesn't actually require it | Pattern: vague-study-attribution language |
| 2026-05-15 | Drafting Discussion | Trigger 6 ("research has shown") | "Research has consistently shown improved patient outcomes with..." | Replaced with specific citation [Cite: PMID:...] | Pattern: citation-implying language without citations |

### Pattern Summary (Update After Each Session)

- Most frequent trigger this session: [Trigger N — description]
- Most frequent subfield triggering captures: [e.g., prior authorization, EHR adoption]
- Most frequent author-name triggering captures: [e.g., a senior author whose name appears across many adjacent papers]
- Sentence constructions to watch: [e.g., "Recent work...", "[Senior author] and colleagues..."]
- Session-end count: [N captures] / [M citations finalized]
- Recognition-to-citation ratio: [N/M] — higher means recognition is engaged

### Trend Across Sessions

| Session date | Captures | Citations finalized | Gate 2 failures | Notes |
|---|---|---|---|---|
| 2026-05-15 | 3 | 4 | 0 | First session — recognition discipline engaged |
| | | | | |

Aim for: many recognition captures, zero Gate 2 failures. That pattern means recognition is fully engaged and the gates are running clean.

---

## Non-Indexed Citations (KFF, CMS, Books, News, Health Affairs Forefront, Preprints)

| # | Publisher | Author/Org | Year | Title | Status | Stable URL | Wayback URL | Access Date | Claim Supported | Gate 4 | Cleared | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | CMS | CMS | 2024 | CMS-0057-F Final Rule | non-indexed | https://www.cms.gov/... | https://web.archive.org/... | 2026-05-15 | "CMS requires 7-day prior auth response" | PASS | ✓ | Load-bearing for policy timeline claim |
|   |   |   |   |   |   |   |   |   |   |   |   |   |

---

## In-Press / Preprint Citations

| # | Title | Author | Status | Verification Source | Expected Pub Date | Notes |
|---|---|---|---|---|---|---|
|   | [Title] | [Author] | in-press | Author confirmation email 2026-05-10 | 2026-Q3 |   |
|   |   |   | preprint | medRxiv DOI 10.1101/... |   | Cite as [Preprint] in Vancouver |

---

## Retired Citations (Removed From Draft But Keep History)

| Original cite | Why retired | What replaced it | Date retired |
|---|---|---|---|
| [Original attempted cite] | No PubMed/Crossref match — likely hallucinated | [PMID of correct replacement] | [date] |
| Doe A. Real paper but didn't support claim. 2020. | Failed Gate 4 (Q1) | PMID:YYY | 2026-05-15 |

---

## Failed Verifications (Audit Trail)

When a citation fails Gate 2 or Gate 4 and is not used, log it here. Pattern detection over time is the value.

| Attempted cite | Failed at | Why | Date |
|---|---|---|---|
|   |   |   |   |

---

## Full Vancouver Reference List

(Generated by `format_citation.py --renumber`. Regenerate at every audit.)

1. [Vancouver entry]
2. [Vancouver entry]

---

## Self-Citation Check (Pre-Submission)

Run `audit_manuscript.py --self-citation-check --author "[your surname]"` and record results:

- Total citations: N
- Self-citations: M
- Self-citation ratio: M/N = X%
- Discussion-section self-citations: K
- Flag if: ratio >20% or Discussion anchored on prior author work

---

## Word-Count Check (Pre-Submission)

Run `audit_manuscript.py --word-count` and record:

- Target: [3,500 / 1,500 / 5,000 / 2,500]
- Actual: [N]
- Status: under / at / over limit

---

## Reviewer-Conflict Manual Check (Pre-Submission)

Manual check item — the skill does not automate this.

- [ ] Reviewed potential reviewer list against citation list
- [ ] Flagged any reviewer-as-cited-author conflicts to editor in cover letter
- [ ] Identified suggested reviewers without conflicts

---

## Notes for This Project

- [Any project-specific citation conventions]
- [Any citations needing full-text retrieval still pending]
- [Any failed verifications worth revisiting]

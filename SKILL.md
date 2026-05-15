---
name: scientific-writing
description: Scientific article writing with iterative citation verification, hallucination detection, Vancouver formatting, and register adaptation between peer-review and trade/long-form contexts. No shortcuts — short pieces and long pieces apply the same discipline; a single fabricated citation in a 1,500-word brief communication is the same reputation-ending event as one in a 5,000-word research article. Trigger whenever the user mentions "scientific article", "peer-reviewed paper", "methodology paper", "research paper", "manuscript", "brief communication", "citation check", "verify citations", "fact-check this draft", "is this citation real", "format citations", "Vancouver", "reference list", "in-line citations", "audit my draft", "literature review", "discussion section", "methods section", "Background and Significance", "results section", "abstract draft", "revise the manuscript", "co-author sent me a draft", or any request to write or edit prose where claims need to be tied to sources. Also trigger automatically when working in any directory containing a citation_log.md file. Verify before write, not after — the iterative loop is the point. Do NOT use for purely architectural/outline conversations where no prose is being committed.
---

# Scientific Writing

A skill for writing where claims must tie to sources. Two registers — **peer-reviewed** (journal articles, methodology papers) and **long-form** (book chapters, substantive essays, trade journalism with citations) — share the same citation discipline. This skill owns register, structure, citations, and the iterative verification loop that prevents hallucinated references.

## Why This Skill Exists

LLM-assisted writing has a specific, well-documented failure mode: confident-sounding citations that don't exist, or that exist but don't say what the prose claims. The pattern is combinatorial — real title plus real journal plus real year plus fabricated authors, or real paper plus wrong claim. Casual review misses these. Peer review may catch them, but only after they've shaped the argument and damaged credibility.

The fix isn't a better citation checker at the end. It's a discipline that runs from the first sentence: catch fabrication at the moment of generation, before it shapes the argument. This skill operationalizes that discipline through five verification gates, an upstream recognition-capture practice, and a final dual-path verification before submission.

## Session-Start Protocol (Mandatory)

Before drafting or editing any prose in a session:

1. **Look for `citation_log.md` in the working directory.** If present, read it — it is the source of truth for what has already been verified.
2. **Look for a previous version of the manuscript.** If present, the session is a revision — the diff-aware workflow applies (see "Revisions" below).
3. **If no log exists and the project is new**, copy `assets/citation_log_template.md` to the project directory as `citation_log.md` before adding the first citation.
4. **Confirm the register** (peer-reviewed vs. long-form) if not already declared in the log's header.
5. **Confirm whether AI disclosure tracking is on** — for peer-reviewed submissions this is typically mandatory. See "AI Use Disclosure" below.

Skipping the session-start protocol is the most common way the discipline collapses. Don't skip it.

## The Core Rule

**Verify every citation when it is added, not at the end.** End-stage citation audits catch errors after they have shaped the argument. The fix is structural — verification is part of writing, not a separate phase.

If a citation cannot be verified at the moment it is written, it goes in as `[UNVERIFIED: claim summary]` and gets verified before the next paragraph. No exceptions, including in short pieces.

**No shortcuts for short pieces.** A 1,500-word brief communication or a 2,000-word essay applies the same five-gate verification as a 5,000-word research article. The reputational consequence of a fabricated citation is the same regardless of word count.

**Never write a PMID, DOI, or any identifier from memory.** This is the most insidious failure mode for AI-assisted scientific writing. Training data contains many PMIDs paired with paper descriptions, and an LLM can produce a confident PMID-paper pairing that turns out to be wrong — the PMID resolves to a completely different paper than the LLM described. The fix: every identifier (PMID, DOI, PMC ID) gets retrieved fresh from PubMed via the PubMed MCP connector or `verify_citation.py` in the current session. "Knowing" an identifier from training data is not knowledge — it is a hallucination waiting to be discovered.

## Recognition Capture (The Upstream Discipline)

The verification gates catch what was already written. Recognition capture catches what was about to be written. This is the discipline that makes everything downstream of it lighter.

Six recognition triggers — when any fires, STOP before completing the sentence:

1. **About to write an identifier** (PMID, DOI, PMC ID) — was it retrieved in this session, or "remembered" from training data?
2. **About to write a specific number or effect size** — verified source, or plausible-sounding number?
3. **About to describe a specific study** ("a 2018 RCT showed...") — verified source, or pattern-matching what such a paper would say?
4. **About to attribute a position to a named author** — verified attribution, or borrowing a well-known name to anchor a general claim?
5. **About to write a date or temporal anchor** — confirmed against source?
6. **About to write "research has shown" / "studies suggest"** — specific citations ready, or citation-implying language without citations?

When any trigger fires, the resolution is one of three: **retrieve** the verified content, **placeholder** with `[UNVERIFIED:]`, or **rewrite** to not require the unverified element.

Log every catch in the Recognition Capture Log section of `citation_log.md`. The log is diagnostic — patterns reveal which subfields, authors, and sentence constructions trigger the most captures, so the discipline gets sharper over time.

Read `references/recognition-capture.md` for the full protocol.

## Decision: Which Register

Two registers. Pick once at the start of the project, document it in the log header, then keep it consistent.

| Signal | Peer-reviewed register | Long-form register |
|---|---|---|
| Target | Peer-reviewed journal | Book chapter, substantive essay, trade journalism with citations |
| Structure | IMRaD or "Background and Significance" extension | Narrative spine, evidence as scaffolding |
| Citation density | High; every empirical claim cited | Selective; citations where they earn their place |
| Method detail | Reproducibility-grade | Sufficient for trust, not for replication |
| Voice load | Scholarly translation register | Narrative translation register |

When in doubt, ask the user. If the target venue has been specified, that determines the register.

Read the relevant register file before drafting:
- Peer-reviewed → `references/peer-reviewed-register.md`
- Methods section specifically → `references/methods-section-protocol.md`
- Long-form (book, essay, trade journalism) → `references/long-form-register.md`
- Non-PubMed/Crossref sources (gray literature, government reports, books, news) → `references/non-indexed-sources.md`
- Dual-path verification protocol (Final Iterative Pass) → `references/dual-path-verification.md`
- Recognition capture (upstream discipline) → `references/recognition-capture.md`

## The Writing Loop — Five Gates

Each gate runs continuously during drafting, not as a phase. Skip none, including for short pieces.

### Gate 1: Claim → Source

Every empirical claim has a source attached at the moment it is written. Four legitimate forms:

1. **Verified citation (indexed)** — PMID, DOI, or full Vancouver reference confirmed via PubMed.
2. **Verified citation (non-indexed)** — gray literature, government reports, books, news articles. Verified manually per `references/non-indexed-sources.md`. Recorded with full URL + access date + verification method.
3. **Unverified placeholder** — `[UNVERIFIED: brief claim]` — must be cleared before the next paragraph.
4. **Explicitly uncited** — author's own observation, framing, or interpretation, stated as such by voice signal: "What I have seen in my own work is..." not a citation.

A claim with no source and no placeholder is a hallucination waiting to be discovered. Stop writing and resolve it.

### Gate 2: Source → Verification

Run `scripts/verify_citation.py` with whichever identifier is available. The script returns PASS / FLAG / FAIL based on title, author list (the discriminator), journal, and year. The signature hallucination pattern — real title + real journal + real year + fabricated authors borrowed from adjacent papers — is caught by the author-list check.

For non-indexed sources, the verification protocol is different but no less rigorous. See `references/non-indexed-sources.md`.

For preprints and "in press" citations, see "In-Press and Preprint Handling" below.

For non-Western author names that FLAG only on author match, re-run with `--name-order family-first` (handles South Asian, Hungarian, East Asian naming conventions).

### Gate 3: Verification → Format

Once verified, format the citation in Vancouver style (`references/vancouver-style.md`):

- Inline: superscript number, before the period
- Numbered in **order of first appearance anywhere** — including tables, figure legends, and box callouts. The `format_citation.py --renumber` script scans tables and figures as well as prose.
- Same citation reused → same number, not a new one.

`scripts/format_citation.py --renumber` handles renumbering on demand. Do not renumber by hand.

### Gate 4: Format → Fact Match (MANDATORY)

Verifying that a paper *exists* is not the same as verifying that it *says what the prose claims*. This gate is mandatory and must be walked through explicitly for every load-bearing citation.

For every verified citation, walk through this checklist and record the result in the citation log:

- [ ] **Q1: Does the abstract support the claim being made?**
- [ ] **Q2: Is the claim within the paper's scope?** (Population, setting, outcome, time period must match.)
- [ ] **Q3: Are effect sizes, populations, or settings represented accurately?**
- [ ] **Q4: For load-bearing citations, has the full text been reviewed?**

If any question returns no: weaken the claim, find a better source, or remove the claim. Do not paper over with hedging language.

A citation logged with Gate 2 PASS but no Gate 4 result is not cleared for submission.

Read `references/fact-check-loop.md` for the full protocol.

### Gate 5: Voice Check

After the section is drafted, review for register fit. Anti-patterns to watch for in scientific writing:

- **Academic creep** — peer-reviewed register adjusts toward scholarly, but translator voice should still preserve accessibility.
- **Credentialing language** — "As a physician..." "Our extensive experience..." Authority should come from what the sentence shows, not from what it claims.
- **Hedging stack** — "may possibly suggest that perhaps." Calibrate hedging to confidence, vary the verb, don't stack.
- **Citation-as-armor** — three citations after a single claim where one would do. Often signals an unconfident author.
- **Lecture register** — addressing the field, not the reader. Translation register requires a reader-in-mind.
- **Filler intensifiers** — "Importantly," "Notably," "Crucially," "It is well-known that..." These add words without adding substance. Cut them.
- **Vague openers** — "Recent advances have..." "In today's world..." "It has long been known..." Open with substance, not throat-clearing.
- **Passive escape from accountability** — "It has been suggested that..." (by whom?). Either attribute or own the claim.
- **Distance from your own findings** — "The data appear to suggest that perhaps..." If you ran the study, you can say "We found."

`[CUSTOMIZE: Add your own voice notes here — your banned constructions, preferred phrasings, register-specific rules. See CUSTOMIZATION.md section 3 for guidance.]`

## Final Iterative Pass (Before Submission)

After all five gates have been walked during drafting, before final formatting, run the **dual-path verification** as the last iterative pass.

### Why two paths

Gate 2 used `verify_citation.py`, which calls PubMed E-utilities and Crossref via the script. The Final Iterative Pass re-verifies every citation through an **independent verification path** (the PubMed MCP connector for Claude users, or manual PubMed.gov search for non-Claude users).

A citation that passes BOTH paths is genuinely verified. A citation that passes one but not the other is the highest-priority flag for manual review — disagreement is the most reliable signal that something is off.

See `references/dual-path-verification.md` for the full protocol.

### Final Formatting (After Dual-Path Verification)

Final formatting is the last step before submission, and only after dual-path verification clears every citation:

1. **Renumber:** `format_citation.py --renumber manuscript.md --out manuscript_final.md`
2. **Generate reference list:** auto-generated at the end by the renumber script
3. **Word-count check:** `audit_manuscript.py manuscript_final.md --word-count --limit [journal limit]`
4. **Self-citation check:** `audit_manuscript.py manuscript_final.md --self-citation-check --author "[your surname]"`
5. **Numbering integrity:** full `audit_manuscript.py manuscript_final.md`
6. **AI disclosure statement:** generate from the citation log's AI Use section
7. **Manual checks:** reviewer-conflict awareness, IRB statement, code/data availability — not automatable but the log template has checkbox items

A manuscript that has not passed the Final Iterative Pass is not ready for submission.

## Scripts

| Script | When |
|---|---|
| `verify_citation.py` | Every time a citation is added inline — Gate 2 |
| `verify_citation.py --name-order family-first` | When an author-only FLAG appears on a non-Western name |
| `format_citation.py --pmid X` | Get a Vancouver-formatted reference entry for a single source |
| `format_citation.py --renumber` | Renumber, generate reference list, or pre-submission |
| `audit_manuscript.py` | Before submission, before sending to a co-author, after revisions, or when inheriting a draft |
| `audit_manuscript.py --diff old.md new.md` | Revision workflow — audit only what changed |
| `audit_manuscript.py --self-citation-check --author "[surname]"` | Pre-submission — flag self-citation creep |
| `audit_manuscript.py --word-count --limit N` | Pre-submission — check against journal word limits |

**Network requirement:** Scripts call `eutils.ncbi.nlm.nih.gov` (PubMed E-utilities) and `api.crossref.org`. Both are free and require no API key.

## The Citation Log

Every project maintains a citation log in the project directory. Template at `assets/citation_log_template.md`.

The log records:
- PMID/DOI or non-indexed identifier
- Full Vancouver reference
- Status: indexed / non-indexed / in-press / preprint / retired
- Which claim it supports
- Gate 2 verification (Path A — script)
- Gate 4 fact-match result
- Path B verification (Final Iterative Pass)
- Cleared-for-submission flag
- AI-use tracking section
- Recognition Capture Log

The log is the source of truth. A citation in the draft but not in the log is suspect.

## Non-Indexed Sources

Sources that PubMed and Crossref don't cover need their own discipline:
- Foundation reports, think-tank briefs
- Government regulatory documents
- Books that aren't journal articles
- News investigative reporting
- Gray literature, preprints not on indexed servers

Verified manually per `references/non-indexed-sources.md`. No less rigorous than indexed citations; just a different pipeline.

## In-Press and Preprint Handling

- **"In press"** — verify via author correspondence or journal accepted-articles list. Log as "in-press" with verification source.
- **Preprints** — cite as `[Preprint]` explicitly. Verify the preprint server record via DOI. Do not cite preprints as if peer-reviewed.
- **Retracted** — never cite without explicit framing that the work was retracted.

## AI Use Disclosure

Most peer-reviewed journals now require explicit disclosure of AI use in writing. The skill tracks what the LLM actually did so the disclosure statement is accurate.

The citation log header includes an "AI Use" section. Update each session with:
- What the AI was used for
- Which sections were AI-assisted
- Which AI system and version

A template draft disclosure statement is in `assets/citation_log_template.md`.

## Revisions: Diff-Aware Workflow

`audit_manuscript.py --diff old_version.md new_version.md` produces:
- New citations → must pass full Gate 2 + Gate 4
- Removed citations → marked RETIRED in log
- Citations whose role changed → re-walk Gate 4 with new claim
- Unchanged citations → no re-verification needed

## Co-Author Draft Intake

When a co-author sends a draft:

1. Run `audit_manuscript.py` immediately — handles both `[Cite: PMID:xxxx]` placeholders and pre-numbered Vancouver references.
2. Flag every citation that fails Gate 2.
3. Do not assume co-author citations were verified.
4. Walk Gate 4 explicitly on every citation supporting claims you're putting your name on.

## Word-Count Discipline

Common journal limits (verify against current author guidelines):
- Research article: ~3,500 words
- Brief communication: ~1,500 words
- Review article: ~5,000 words
- Perspective: ~1,500–2,500 words

`audit_manuscript.py --word-count` counts body text (excludes title, abstract, references, tables, figure legends, acknowledgments).

## Self-Citation and Reviewer-Conflict

**Self-citation creep.** Citing one's own prior work is appropriate in Introduction for situating contribution. Suspect in Discussion as load-bearing evidence. `audit_manuscript.py --self-citation-check --author "[your surname]"` flags when >20% of citations are self-citations or when Discussion is anchored on prior author work.

**Reviewer-conflict awareness.** Most journals require flagging conflicts when citing potential reviewers' work. Manual check item.

## Failure Modes

1. **Citation drift** — paragraph cites a paper supporting an adjacent but not identical claim. Detected at Gate 4.
2. **Stack-of-citations** — three or four citations after a single claim, none alone supporting it. Weaken or find a better source.
3. **Self-citation creep** — see above.
4. **Adjacent-author hallucination** — fabricated author names that sound right. Caught by author-list check.
5. **Year shift** — citing right paper but wrong year. Caught by format script.
6. **International name parsing failures** — `--name-order family-first` flag handles these.
7. **Co-author draft hallucinations** — audit on intake.
8. **Revision drift** — sharpened claims no longer match cited paper. Caught by diff-aware re-audit.

## When This Skill Does NOT Apply

- **Internal memos, dashboards, decision docs** — no citation discipline needed
- **Fiction, creative work** — different skill
- **Pure architectural conversation** — outlining, brainstorming, debating thesis without committing prose

## Operating Discipline

This skill exists because writers in academic and journalistic venues face credibility-ending consequences for fabricated citations. The discipline does not scale down for short pieces — a 1,500-word brief communication with one hallucinated citation is the same reputational event as a 5,000-word article with one.

When in doubt: stop writing, run verify, log it, walk Gate 4, then resume. Slower is faster.

---

## Customization

See `CUSTOMIZATION.md` in the repo root for the five places to adapt this skill to your own work:
1. Target venue / register names
2. Self-citation author surname
3. Voice notes (Gate 5)
4. AI system + version (disclosure)
5. Methods section example data

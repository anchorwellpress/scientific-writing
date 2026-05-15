# scientific-writing

A skill for AI-assisted scientific writing where citations must be real.

## What This Is

A discipline and toolkit for writing peer-reviewed articles, long-form essays, and trade journalism with AI assistance — without hallucinated citations entering your prose. Five verification gates run during writing (not at audit). An upstream "recognition capture" practice catches fabrication-prone moments before they enter prose. A dual-path verification at submission compares two independent verification routes; disagreement between them is the most reliable hallucination signal.

LLM-assisted citation generation has documented hallucination rates ranging from ~30% (GPT-4, citations in natural sciences) to 91% (Bard, against systematic reviews).¹ ² The pattern is specific: real title, real journal, real year, fabricated authors borrowed from adjacent papers. Casual review misses it. Peer review may catch it, but only after credibility is at stake. This skill is built to catch it earlier.

## Who This Is For

Three audiences with different value propositions:

1. **Claude users** — install as a skill; full automated dual-path verification using the PubMed MCP connector.
2. **Other LLM users (ChatGPT, Gemini, etc.)** — use the Python scripts standalone; apply the discipline manually using the reference files and templates as a workflow.
3. **Non-AI writers** — the reference files, citation log template, and audit scripts work as a writing-discipline toolkit even without an LLM. Vancouver formatting, recognition capture, and the five-gate model are method, not tooling.

## What's Inside

```
scientific-writing/
├── SKILL.md                                — The discipline, top to bottom
├── CUSTOMIZATION.md                        — Five places to adapt to your work
├── LICENSE                                 — MIT
├── references/
│   ├── peer-reviewed-register.md           — IMRaD conventions, journal expectations
│   ├── long-form-register.md               — Book, essay, trade journalism conventions
│   ├── methods-section-protocol.md         — Methods-section specifics
│   ├── vancouver-style.md                  — Citation formatting reference
│   ├── citation-verification.md            — Hallucination failure modes
│   ├── fact-check-loop.md                  — Gate 4 (does the paper say what you claim)
│   ├── dual-path-verification.md           — Final Iterative Pass before submission
│   ├── recognition-capture.md              — The upstream discipline
│   └── non-indexed-sources.md              — Foundation reports, gov docs, books, news
├── scripts/
│   ├── verify_citation.py                  — Path A: PubMed E-utilities + Crossref
│   ├── format_citation.py                  — Vancouver formatting, renumbering
│   └── audit_manuscript.py                 — Bulk audit, diff, self-citation, word count
└── assets/
    ├── citation_log_template.md            — Full per-project citation log
    └── recognition_capture_template.md     — Lightweight log for short pieces
```

## Quick Start

### For Claude users (skill install)

```bash
# Place in your skills directory
cp -r scientific-writing/ /path/to/your/skills/
```

The skill triggers automatically on phrases like "write a manuscript", "verify this citation", "audit my draft", or whenever you're working in a directory containing `citation_log.md`.

### For other LLM users / standalone use

The Python scripts run independently. Requirements: Python 3.9+, internet access to PubMed E-utilities and Crossref (both free, no API key).

```bash
# Verify a citation by PMID
python scripts/verify_citation.py --pmid 29346583

# Get Vancouver-formatted reference entry from PMID
python scripts/format_citation.py --pmid 29346583

# Audit a draft manuscript
python scripts/audit_manuscript.py manuscript.md

# Diff-aware revision audit
python scripts/audit_manuscript.py --diff old_version.md new_version.md

# Self-citation check
python scripts/audit_manuscript.py manuscript.md --self-citation-check --author "Smith"

# Word-count check
python scripts/audit_manuscript.py manuscript.md --word-count --limit 3500
```

### For non-AI writers

Read `SKILL.md` for the discipline. Copy `assets/recognition_capture_template.md` into your project. The reference files (Vancouver style, fact-check loop, register guidance) work as a manual writing toolkit. The audit scripts work on any markdown manuscript.

## The Core Discipline (Five Gates + Recognition Capture)

**Recognition Capture** runs *during* writing. Six triggers — about to write a PMID, a specific effect size, a study description, an author attribution, a date, or "research has shown" — stop you before fabrication enters prose. Resolution: retrieve a verified source, write `[UNVERIFIED:]` placeholder, or rewrite to not need the unverified element.

**Gate 1: Claim → Source.** Every empirical claim has a source attached when written.

**Gate 2: Source → Verification.** Run `verify_citation.py`. Returns PASS / FLAG / FAIL. Author-list match is the discriminator for the most common LLM hallucination pattern (real title/journal/year + fabricated authors).

**Gate 3: Verification → Format.** Vancouver formatting; auto-renumbering on demand.

**Gate 4: Format → Fact Match.** Does the paper actually support the claim? Walk Q1-Q4 explicitly. Mandatory for load-bearing citations.

**Gate 5: Voice Check.** Anti-patterns: academic creep, credentialing language, hedging stacks, citation-as-armor, lecture register.

**Final Iterative Pass.** Re-verify every citation through an independent path before submission. For Claude users, this is the PubMed MCP connector. For others, manual PubMed.gov search. Disagreement between paths = highest-priority flag.

## Customization

This skill ships fully sanitized. To adapt to your work, see `CUSTOMIZATION.md` for the five places to edit:

1. **Target venue and register details** (`SKILL.md`, `references/peer-reviewed-register.md`)
2. **Self-citation author surname** (`assets/citation_log_template.md`)
3. **Voice notes** (Gate 5 anti-patterns specific to your writing)
4. **AI system + version** (disclosure template)
5. **Methods section example data** (your typical data sources, frameworks)

All customization points are marked with `[CUSTOMIZE: ...]` in the files.

## What This Skill Does NOT Cover

- Word/PDF document conversion — use a separate tool
- Submission systems (Editorial Manager, ScholarOne) — the skill prepares your manuscript for submission; you submit
- Co-author coordination tools — the skill helps audit inherited drafts but doesn't manage co-author workflow
- Internal memos, dashboards, decision documents — the discipline is overhead for these
- Fiction, creative non-citing work — different problem

## Network Requirements

`verify_citation.py` and `format_citation.py` call:
- PubMed E-utilities: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`
- Crossref API: `https://api.crossref.org/works/`

Both are free and require no API keys. If you're running in a sandboxed environment with network restrictions, add these to your allowed domains.

## Why a During-Writing Discipline

Most existing tools for AI-assisted scientific writing work at one of two moments:

- **Before writing** — research lookup tools that retrieve papers and feed them to the LLM, then trust the LLM to use them correctly
- **After writing** — citation checkers that scan a finished manuscript and flag invalid references

Both miss the moment that matters most. A fabricated citation that survives the writing phase has already shaped the paragraph it sits in. By the time an end-stage checker flags it, the prose has been built around a falsehood. Removing the citation means rebuilding the paragraph.

This skill works at the **third moment** — the one most tools skip. It runs *during* writing, sentence by sentence, while prose is being committed. Recognition capture catches fabrication at the moment of generation, before the sentence finishes. The five gates run continuously, not at audit. The dual-path verification re-checks every citation before submission, but only after the discipline has already caught most fabrications upstream.

This is not "another citation checker." Checkers and document generators are useful for the moments they cover. This skill covers a different moment, and it is incompatible with the assumption that verification can wait. If your workflow currently writes a draft first and verifies citations afterward, this skill changes that order. That is the point.

## What This Skill Does NOT Replace

**Scientific rigor still applies.** The five gates and recognition capture make the discipline *easier to keep* — they do not perform it for you. Specifically:

- **Author accountability is unchanged.** Every citation under your name is still your responsibility. Every claim those citations support is still your responsibility. Every word of the prose around them is still your responsibility. The skill does not absorb any of that responsibility — it lowers the friction of meeting it.
- **Gate 4 (fact-match) is not automated.** Verifying that a paper *exists* is automated. Verifying that the paper *says what the prose claims* requires reading the paper. The Gate 4 checklist structures the reading; it does not replace it.
- **Dual-path verification reduces false negatives, not human review.** A citation that passes both paths still needs to be appropriate for the claim, situated correctly in the discussion, and not over- or under-cited. Those are judgments the writer makes.
- **Peer review remains the gold standard.** This skill reduces what peer reviewers have to catch about citation integrity. It does not reduce what they catch about study design, statistical analysis, claim interpretation, or scientific contribution.

Use this skill to keep AI-assisted writing honest at the moment of generation. Use everything else you already use — peer review, advisor feedback, statistical consultation, editorial review — for everything else.

## What This Skill Does NOT Do

To be honest about scope:

- **Does not generate publication-ready PDFs, LaTeX, or posters.** Output is markdown with Vancouver-formatted citations. Use a separate document-generation tool for the final artifact, *after* the discipline has cleared the citations.
- **Does not search the literature for you.** It verifies citations you (or your LLM) put forward. Literature search is a separate workflow upstream.
- **Does not generate figures, schematics, or diagrams.** Out of scope.
- **Does not audit against reporting guidelines** (STARD, STROBE, PRISMA, etc.). Other tools do that well; pair this skill with one of them if you need both.
- **Does not work if you only invoke it after the draft is finished.** The discipline is structurally tied to writing-time application. Running it as a post-hoc audit catches existence-class hallucinations but misses everything recognition capture is designed to prevent.

## Contributing

Pull requests welcome. The most valuable contributions are:

- **Additional venue-specific reference files** (e.g., `references/[journal]-register.md` for journals with unusual house styles)
- **Better hallucination test cases** — known failure patterns you've encountered
- **Improvements to script accuracy** — particularly the international name parsing and the title fuzzy-match tolerance

When contributing, please test against `scripts/audit_manuscript.py` on a sample manuscript with deliberately seeded errors (Class 1 fabrication, Class 2 plausible-wrong-authors, Class 3 real-paper-wrong-claim).

## Related Work

Several tools address adjacent problems in this space. K-Dense's [claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) is an end-to-end document-production toolkit covering papers, posters, and grant proposals with real-time literature search. Medical Research Skills ([hesreallyhim/awesome-claude-code#1389](https://github.com/hesreallyhim/awesome-claude-code/issues/1389)) provides reporting-guideline compliance auditing (STARD, STROBE, PRISMA, ARRIVE, TRIPOD+AI). CheckIfExist offers web-based reference validation against CrossRef, Semantic Scholar, and OpenAlex. clibib retrieves authoritative BibTeX records via Zotero Translation Server.

This skill operates at a different moment in the writing workflow than any of these. Production tools generate documents; checkers validate finished citation lists; this skill enforces verification *during* prose drafting, when the citation is going into the paragraph. The discipline complements rather than competes with end-stage tools — a manuscript drafted under this discipline still benefits from a finished-document audit before submission.

## License

MIT. See `LICENSE`.

## Acknowledgments
Built on documented hallucination patterns from peer-reviewed LLM citation studies (Mugaanyi 2024,¹ Chelli 2024²). The discipline draws on standard scientific writing practice — IMRaD, Vancouver style, fact-checking discipline — adapted for AI-assisted workflows.
---
According to PubMed:

¹ Mugaanyi J, Cai L, Cheng S, Lu C, Huang J. Evaluation of Large Language Model Performance and Reliability for Citations and References in Scholarly Writing: Cross-Disciplinary Study. *J Med Internet Res.* 2024;26:e52935. [doi:10.2196/52935](https://doi.org/10.2196/52935)
² Chelli M, Descamps J, Lavoué V, et al. Hallucination Rates and Reference Accuracy of ChatGPT and Bard for Systematic Reviews: Comparative Analysis. *J Med Internet Res.* 2024;26:e53164. [doi:10.2196/53164](https://doi.org/10.2196/53164)

² Chelli M, Descamps J, Lavoué V, et al. Hallucination Rates and Reference Accuracy of ChatGPT and Bard for Systematic Reviews: Comparative Analysis. *J Med Internet Res.* 2024;26:e53164. [doi:10.2196/53164](https://doi.org/10.2196/53164)

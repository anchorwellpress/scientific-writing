# Dual-Path Verification (Final Iterative Pass)

Path A and Path B are two independent verification routes against PubMed. Both passing means the citation is genuinely verified. Disagreement between them is the most reliable hallucination signal we have.

## Why Two Paths

A single verification path has known failure modes:
- Fuzzy-match thresholds may pass borderline cases that shouldn't pass
- API edge cases (caching, intermittent record updates) can produce false confirms
- A single-path verifier can be defeated if the fabricated reference happens to share enough surface features with a real one

Dual-path verification mitigates these by using independent infrastructure with different query semantics. The two paths produce agreement on real citations and disagreement on subtly hallucinated ones.

## Path A: `verify_citation.py` (Script)

- Calls PubMed E-utilities (esummary, efetch, esearch) and Crossref directly.
- Uses fuzzy title matching, exact year matching, and **author-list discriminator** (the primary catch for Class 2 hallucinations).
- Returns PASS/FLAG/FAIL based on title, author list, journal, year.
- Runs continuously during drafting (Gate 2).

## Path B: PubMed MCP Connector

- Calls PubMed via Anthropic's MCP infrastructure.
- Three relevant tools:
  - `PubMed:get_article_metadata` — verify a known PMID
  - `PubMed:search_articles` — verify a citation by title + author + year search
  - `PubMed:get_full_text_article` — pull full text from PubMed Central for Gate 4 fact-check
- Runs once per citation in the **Final Iterative Pass**, after all drafting is complete.

## The Final Iterative Pass Protocol

For every citation in the citation log:

### Step 1: Establish the canonical PMID (if known)

If the citation log has a PMID, query `PubMed:get_article_metadata` with that PMID. The response includes:
- Title
- Author list with full names
- Journal
- Publication year and date
- DOI
- Abstract
- PMC ID (if available — needed for full-text retrieval)

Compare against the citation log entry:
- **Title match** — must be exact (allow for minor punctuation differences)
- **Author list match** — first author surname must match; full overlap is strong PASS; partial overlap is FLAG
- **Journal match** — exact (PubMed uses canonical abbreviations)
- **Year match** — exact

### Step 2: If no PMID, search by title + first author

Use `PubMed:search_articles` with query syntax:

```
"[exact title]"[Title] AND [First Author Surname][Author]
```

Or for fuzzier matching when title parsing might be imperfect:

```
[Key title terms] AND [First Author Surname][Author] AND [Year][Date - Publication]
```

If the search returns exactly one result that matches the citation's title and authors, Path B = PASS. If multiple results, examine each. If zero results, Path B = FAIL.

### Step 3: For load-bearing citations, pull full text

Citations that the argument depends on need Gate 4 verification against the full paper, not just the abstract.

If the article has a PMC ID:
```
PubMed:get_full_text_article(pmc_ids=["PMC######"])
```

This returns the full article text. Search it for:
- The specific claim being made in the manuscript
- The exact effect size or population statistic being cited
- The setting (study site, population, time period) the manuscript attributes to it

If the article does not have PMC full text, note this in the log. Gate 4 will be limited to abstract-level review.

### Step 4: Record both Path A and Path B in the citation log

Update the citation log to record both verifications:

| # | PMID | First Author | Path A (date, verdict) | Path B (date, verdict) | Final | Notes |
|---|---|---|---|---|---|---|
| 1 | [PMID] | [Author] | PASS ([date]) | PASS ([date], MCP) | CLEARED | Gate 4 full-text confirmed via PMC |

## Reconciling Disagreements

Four disagreement patterns, in order of severity:

### Pattern 1: Path A PASS + Path B PASS → CLEARED

Both paths agree the citation is real and matches. Proceed to formatting.

### Pattern 2: Path A FLAG + Path B PASS → review Path A

Path A's fuzzy matching might have flagged a title variation (e.g., subtitle handling differs between the script's parser and PubMed's record) or author-list partial match. Re-examine the Path A output:
- If the FLAG was on title fuzzy match and Path B confirms the exact match, accept Path B's result.
- If the FLAG was on author list (e.g., 80% overlap rather than 100%), examine each missing or extra author against the canonical record. Citation log entry may need correction.
- Document the reconciliation in the log.

### Pattern 3: Path A FAIL + Path B PASS → Path A caught something

Path A's stricter author-list discriminator is more sensitive to Class 2 hallucinations than Path B's broader search. This pattern means:
- The citation might be a Class 2 hallucination that Path B's search returned a different (real) paper for
- Or the citation is real but the manuscript's author list is wrong
- Path A's `--name-order family-first` might resolve the discrepancy

Resolution: pull the actual paper Path B returned and compare against the manuscript's claimed citation. If the title and journal match but authors differ, the manuscript's author list is wrong — correct it in the citation log. If the title doesn't match, Path B returned a different paper; Path A's FAIL stands.

### Pattern 4: Path A PASS + Path B FAIL → HIGHEST PRIORITY

This is the most concerning disagreement. The script-based path passed something that PubMed's MCP infrastructure can't find. Possibilities:

- Path A used cached or stale PubMed E-utilities data
- The script's fuzzy match was too lenient
- The citation is real but indexed in a way the MCP search doesn't catch (rare)
- The citation is hallucinated and Path A failed to catch it

Resolution: manual verification required. Search PubMed.gov directly with the citation's title in quotes. If found, both paths should have found it — investigate why one didn't. If not found, the citation is likely hallucinated; do not submit.

### Pattern 5: Both FAIL → STRONG HALLUCINATION SIGNAL

Independent verification by two paths returns no match. Treat as hallucinated unless the citation is plausibly non-indexed (book, KFF report, CMS document) — in which case it should have been flagged as NONINDEXED from the start, not run through PubMed verification at all.

## When to Use Path B Only (Skipping Path A)

Path B is sufficient on its own only for:
- Re-verifying a citation already known to be in PubMed (e.g., the manuscript inherited a PMID from a co-author and you just need to confirm)
- Pulling full text for Gate 4 review
- Searching for a potential replacement citation when one fails

In all other cases, Path A runs first (during drafting) and Path B runs as the final pass.

## When Path A Is Sufficient (Skipping Path B)

Path B should not be skipped for any peer-reviewed submission. The cost of one MCP call per citation is trivial compared to the reputational risk of a hallucinated reference.

For long-form pieces and trade journalism, Path A alone is acceptable IF:
- The citation list is short (under 15 citations)
- No citation is load-bearing for a contestable claim
- The piece is not under journalistic fact-check scrutiny

For anything going to a journal, Path B always runs.

## Logging the Final Iterative Pass

The citation log's "Final Iterative Pass" section records:

- Date of pass
- Citations cleared (Path A PASS + Path B PASS)
- Disagreements found and how each was resolved
- Citations dropped or replaced as a result of disagreement
- Full-text reviews performed for load-bearing citations
- AI disclosure statement updated to reflect the dual-path verification

A manuscript without a completed Final Iterative Pass entry in the log is not cleared for submission.

# Citation Verification Protocol

Two well-documented hallucination failure modes in LLM-assisted scientific writing. Apply both as explicit checks.

## The Two Hallucination Classes

### Class 1: Fabricated Reference

A reference that does not exist at all. Easiest to catch — PubMed and Crossref return no match.

### Class 2: Plausible Reference with Wrong Authors

The signature failure documented in cross-disciplinary studies of LLM citation accuracy. Pattern:
- Title is real and correct
- Journal is real and correct
- Year is real and correct
- Authors are fabricated — names that sound right because they appear on adjacent papers in the same subfield

This passes a casual title-and-journal check. It fails the author-list check.

**Why this happens:** LLMs trained on biomedical text learn that "an article about X in journal Y in year Z is plausibly by these names." They generate from the distribution rather than retrieving from the record. The fix is to verify against the record, not against plausibility.

### Class 3: Real Reference, Wrong Content

The third class — the paper exists, the citation is formatted correctly, but the paper does not actually say what the prose claims. This is Gate 4 in the main skill (`fact-check-loop.md`), not Gate 2. But noted here because the verification script returns abstract text — Gate 2 and Gate 4 can be partly executed together.

## The Protocol

For every citation added inline, run `verify_citation.py` with whichever identifier is available:

```bash
python scripts/verify_citation.py --pmid 29346583
python scripts/verify_citation.py --doi 10.1093/jamia/ocx083
python scripts/verify_citation.py --reference "Smith JA, Jones BC, Doe DE. Title of the paper. J Example Med. 2024;10(2):100-110."
```

The script returns one of:

### PASS
All four elements match a real record:
- Title (within fuzzy match tolerance)
- Author list (last names match, in order)
- Journal
- Year

Citation is verified. Log it.

### FLAG
Partial match. Specifically:
- Title and journal match but authors don't → almost certainly Class 2 hallucination. Treat as FAIL unless you can find the correct authors.
- Title close but not exact → likely a real paper described imprecisely. Open the abstract and reconcile.
- Year off by one → check whether you're citing the publication year or the e-pub year. Use publication year.
- All match but DOI doesn't → DOI was fabricated; use the correct DOI from PubMed.

### FAIL
No match anywhere. Two possibilities:
1. The citation is hallucinated. Most common cause.
2. The citation is real but obscure — a regional journal not indexed in PubMed, an old paper not yet digitized, a non-medical source. Search Crossref, Google Scholar, and the publisher's site before concluding hallucination. If still no match, do not use the citation.

## Manual Verification When Scripts Aren't Available

If `verify_citation.py` cannot run (no network, API down), manual protocol:

1. Open https://pubmed.ncbi.nlm.nih.gov/ and search by title in quotes.
2. If found, click through. Verify: first author, last author, journal, year, volume, pages.
3. If not found, search Crossref at https://search.crossref.org/.
4. If not found, search Google Scholar with title in quotes.
5. If none of the three find it, the citation is unverified. Mark `[UNVERIFIED]` and do not include in submission.

Manual verification is slower but works. It catches every class of hallucination. Do not skip it.

## Known Adjacent-Field Hallucination Risks

Specific subfields where the LLM-distribution hallucination is most common in biomedical writing:

- **Densely-published research areas with a small handful of recurring senior authors** (clinical informatics methodology, healthcare policy, burnout research, AI/CDS, EHR usability). Author names get borrowed across papers easily, and LLMs trained on the densest subfields are most prone to combinatorial fabrication in those subfields.
- **Areas where multi-author papers are the norm**, so any individual senior author appears on many adjacent papers.
- **Areas dominated by a few institutional research groups**, where group-membership names cluster.

When citing in these subfields, **verify the full author list, in order**, not just the first author.

## Verification Log

Every verified citation should be logged. Template in `assets/citation_log_template.md`. The log is the source of truth — at submission time, the log and the reference list should match exactly.

## What to Do When a Citation Fails

1. **Stop writing the section.** Continuing past a failed citation lets it shape the prose around it.
2. **Identify what claim the citation was supporting.** That claim is now unsupported.
3. **Find a real source for the claim.** Search PubMed and Google Scholar with the actual concept, not with the fabricated reference's title.
4. **If no real source exists**, the claim is unsupported. Either revise the claim or remove it. Do not paper over with hedging language ("some have suggested...") — that just creates a new unsupported claim.
5. **Log the failure.** Keep a record of which citations failed and why. Patterns emerge — particular subfields, particular co-author combinations — and the record helps catch them earlier next time.

## The Operational Rule

Verification is faster than recovery. Spending 30 seconds to verify a citation when it is written prevents an hour of remediation when an editor or reviewer flags it. End-stage citation rewrites cost more than the original draft because the audit happens after the fabricated citation has already shaped the argument. Don't run that loop.

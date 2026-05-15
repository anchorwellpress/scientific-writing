[peer-reviewed-register.md](https://github.com/user-attachments/files/27807778/peer-reviewed-register.md)
# Peer-Reviewed Register

For methodology papers, original research, perspectives, and brief communications targeting peer-reviewed journals.

## Structure: IMRaD and Variants

Standard original research follows IMRaD:

- **Abstract** — structured (Objective, Materials and Methods, Results, Discussion, Conclusion). 250 words typical. Every claim in the abstract must be in the body.
- **Introduction / Background and Significance** — frame the gap, not the field. Last paragraph states the specific contribution. Avoid "to the best of our knowledge" framings. Some journals use "Background and Significance" as the second-section header; check current author guidelines and use the journal's preferred form.
- **Materials and Methods** — reproducibility-grade. See `methods-section-protocol.md` for the full Methods protocol including subsection sequence, citation conventions, IRB statement placement, and code/data availability.
- **Results** — observations only. No interpretation. Tables/figures referenced by number.
- **Discussion** — interpret in this order: principal findings, fit with prior literature, mechanisms or explanations, limitations, implications. End on implications, not on a call for "more research."
- **Limitations** — substantive limitations, not boilerplate. A limitations paragraph that lists everything in equal weight signals the author hasn't thought hard about which ones actually matter.

**Methodology papers** (framework descriptions, methods notes): Introduction, Framework Description, Application (case study), Discussion, Conclusion. No Results section.

**Perspectives / Editorials**: argument-driven. Single thesis stated early, evidence assembled to support it, anticipated counterarguments addressed. Citation density still high.

## Tone

Scholarly but not arid. Translation register holds: complex methods explained well, not hidden behind jargon. Active voice where possible — "We extracted..." not "Data were extracted..."

What changes from long-form register:
- Personal observation appears in Discussion, not in Methods or Results.
- No second-person address.
- Hedging is calibrated, not reflexive. "Our data suggest" is appropriate; "It might possibly be the case that perhaps" is not.

## Citation Density and Placement

- Every empirical claim cited. No exceptions.
- Definitions of established concepts: cite the canonical source.
- Method choices: cite the method's original description and any validation study.
- Comparable prior work in Discussion: cite all directly comparable studies, even contradictory ones. Especially contradictory ones.
- Avoid citation stacking (three or four citations after one claim) unless each contributes distinct support.

## Journal-Specific Requirements

Most peer-reviewed journals require:
- Structured abstract
- Specific word counts (verify at submission)
- Vancouver references (or journal's house style — most biomedical journals use Vancouver)
- ORCID for all authors
- Data and code availability statement
- AI use disclosure if AI was used in writing or analysis

`[CUSTOMIZE: Add your target journal's specific requirements here — word limits, structured abstract format, reference style if not Vancouver, any unusual conventions.]`

## Common Mistakes to Avoid

1. **"To the best of our knowledge, this is the first study..."** — almost never true and signals literature-search weakness. State the contribution directly.
2. **"More research is needed."** — uninformative. Specify what research, by whom, and why it would change practice.
3. **Citing reviews instead of primary sources** for specific findings. Cite reviews for context, primary sources for findings.
4. **Reusing the same hedge across the Discussion** — varies the verb, but the cumulative effect is unconvincing. Calibrate hedging to confidence.
5. **Author-self-citation creep** — acceptable in introduction for situating prior work, suspect in Discussion as load-bearing evidence.

## Pre-Submission Checklist

- [ ] Every citation in the body appears in the reference list
- [ ] Every reference in the list is cited in the body
- [ ] Numbering is sequential by first appearance
- [ ] `audit_manuscript.py` returns no FAIL citations
- [ ] Abstract claims all appear in body
- [ ] Limitations paragraph is substantive, not boilerplate
- [ ] Data and code availability statement present
- [ ] ORCID and conflict of interest statements complete
- [ ] AI use disclosure complete (per journal requirements)

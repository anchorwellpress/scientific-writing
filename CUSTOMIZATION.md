# Customization Guide

This skill ships fully sanitized. Five places to adapt it to your own work. All customization points are marked with `[CUSTOMIZE: ...]` in the files. None of these changes break the core verification logic — they make the skill more useful to your specific writing.

Estimated time to complete all five: 15–30 minutes.

## 1. Target Venue and Register Details

**File:** `references/peer-reviewed-register.md`

**Why:** Different journals have different requirements (word limits, structured abstract formats, reference styles, required statements). Adding your target journal's specifics speeds up future drafts.

**What to do:** Find the `[CUSTOMIZE: Add your target journal's specific requirements here ...]` marker. Replace with the specifics for your venue:

```markdown
## Journal-Specific Requirements

For [Your Target Journal]:
- Word limit: [N] for research articles, [N] for brief communications
- Structured abstract format: [Objective / Methods / Results / Conclusions]
- Reference style: Vancouver (or specify)
- Required statements: data availability, conflict of interest, AI use, IRB
- Unusual conventions: [e.g., "Background and Significance" not "Introduction"]
```

If you write for multiple venues, create separate files: `references/journal-A-register.md`, `references/journal-B-register.md`. Reference them from `SKILL.md` under "Read the relevant register file before drafting."

## 2. Self-Citation Author Surname

**File:** `assets/citation_log_template.md`

**Why:** The self-citation check needs to know your surname to flag your own papers in the reference list.

**What to do:** Find this line:

```markdown
Run `audit_manuscript.py --self-citation-check --author "[your surname]"` and record results:
```

Replace `[your surname]` with your actual surname. Example:

```markdown
Run `audit_manuscript.py --self-citation-check --author "Smith"` and record results:
```

For multi-author papers where multiple authors want self-citation tracking, you can run the script multiple times with different `--author` flags.

## 3. Voice Notes (Gate 5)

**File:** `SKILL.md`, under "Gate 5: Voice Check"

**Why:** Voice anti-patterns vary by writer. The default Gate 5 covers common scientific-writing voice problems; your own writing likely has specific patterns to watch for.

**What to do:** Find the `[CUSTOMIZE: Add your own voice notes here ...]` marker. Replace with your specific voice preferences. Examples:

```markdown
[CUSTOMIZE: Add your own voice notes here]:

Banned constructions:
- "Importantly, ..." (filler)
- "It is well-known that ..." (citation evader)
- "Recent advances have ..." (vague opener)

Preferred phrasings:
- Active voice in Methods unless reviewer convention specifically requires passive
- "We found" not "It was found"
- "The data suggest" not "The data suggests" (data is plural)

Register-specific rules:
- For my [target journal] audience, avoid jargon from [other field]
- Methods section can use first-person plural; Results section should not interpret
- Closing paragraph should land on a specific implication, not a generic call for more research
```

The more specific the notes, the more useful Gate 5 becomes.

## 4. AI System and Version (Disclosure)

**File:** `assets/citation_log_template.md`, AI Use Disclosure section

**Why:** Journal disclosure requirements specify the AI system used. The template has a placeholder; fill in what you actually use.

**What to do:** Find this line:

```markdown
**System used:** [e.g., Claude (Anthropic), version Opus 4.7]
```

Replace with the actual system + version you use. Update each session if it changes (model versions change frequently).

Also customize the draft disclosure statement at the bottom of the AI Use section to match your venue's required language. For example, JAMA requires specific phrasing; *Nature* family journals have their own template; some journals require AI use to be in the Methods section, others in Acknowledgments.

## 5. Methods Section Example Data

**File:** `references/methods-section-protocol.md`

**Why:** The Methods protocol has a `[CUSTOMIZE: Add your common Methods patterns here ...]` marker. Filling this with your typical data sources, frameworks, and design templates makes Methods sections come together faster — and avoids re-deriving the same boilerplate every paper.

**What to do:** Find the marker. Add your common Methods patterns. Example:

```markdown
[CUSTOMIZE: Your common Methods patterns]

### My EHR-based cohort studies
- Data source format: "[Your EHR/data warehouse name] (version X), accessed via [tool] on [date range]."
- Standard cohort filters: [list your usual inclusion logic]
- Comparator typically used: [your usual comparator population]
- IRB protocol number: [if a recurring protocol covers this work]

### My survey studies
- Survey platform: [REDCap / Qualtrics / etc.]
- Sampling approach: [your usual approach]
- Response rate calculation: [your usual definition]

### My framework application work
- Frameworks you apply: [list]
- Reviewer panel size: [your usual] with reference to methodology recommendation [citation]
```

The more concrete, the faster future Methods sections come together.

## Optional: Additional Customizations

### Custom Recognition Triggers

If your writing has subfield-specific fabrication risks not covered by the six default triggers, add them to `references/recognition-capture.md` under "The Six Recognition Triggers."

Examples of custom triggers worth adding:
- "About to cite a regulatory document or statute" — these need verification against the actual source, not memory
- "About to cite an industry report" — gray literature has the same hallucination risk
- "About to write a specific quote from a named person" — quotes are high-risk for paraphrase drift

### Custom Vancouver Variations

If your target venue requires a Vancouver variant (e.g., AMA style differs slightly from NLM Vancouver), edit `references/vancouver-style.md` accordingly. Keep the original as `references/vancouver-style-nlm.md` if you write for multiple styles.

### Adding a Non-Vancouver Style

The skill is built around Vancouver but the discipline doesn't require it. If your venue uses APA, Chicago, or another style:

1. Copy `references/vancouver-style.md` → `references/apa-style.md` (or your style)
2. Rewrite the formatting rules for your style
3. Update `SKILL.md` to reference the new style file
4. The `format_citation.py` script currently outputs Vancouver — you may need to modify the output format for non-Vancouver styles (the script has a `format_vancouver()` function that's clearly named for replacement)

## What NOT to Customize

A few elements are core to the discipline and shouldn't change:

- **The five gates** — these are the architecture; rearranging them breaks the verification flow
- **Recognition capture as upstream practice** — the order matters (recognition before gates), don't flip it
- **The Final Iterative Pass via dual-path verification** — this is the safety net; removing it removes the strongest hallucination signal
- **`[UNVERIFIED:]` placeholder convention** — the audit scripts depend on this exact syntax
- **`[Cite: PMID:XXXX]` placeholder convention** — same; the format script depends on it

## After Customizing

Run the audit script on a test manuscript to verify your customizations don't break anything:

```bash
python scripts/audit_manuscript.py [path/to/a/test/manuscript.md]
```

If the script runs cleanly, your customizations are compatible.

## When to Re-Customize

Re-visit your customization file when:
- You start writing for a new venue
- Your AI system or version changes
- You catch a fabrication pattern that recurs (add it as a custom recognition trigger)
- A journal updates its author guidelines or AI disclosure requirements

The skill gets sharper with use. Customization keeps it aligned with how *you* actually write.

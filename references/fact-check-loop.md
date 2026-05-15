# Fact-Check Loop (Gate 4)

Verifying that a paper exists is not the same as verifying that the paper supports the claim being made. Gate 4 is the second verification — content match, not existence match.

## When This Gate Runs

Every time a citation passes Gate 2 (existence verified). The script that verified existence also returned the abstract. Read it.

Three questions, in order:

### Question 1: Does the abstract support the claim being made?

The claim in the prose should be either:
- Directly stated in the abstract
- A reasonable summary of what the abstract reports
- Within the inferential range that the methods support

If the abstract does not contain the claim and does not obviously support it, the citation is wrong even if the paper is real.

**Example failure:** Prose says "30-day readmissions dropped by 22% under the intervention." Abstract says "The intervention was associated with reduced readmissions (p<0.05)" but never gives the 22% number. The claim is overspecified relative to the source. Either find the exact number (full text may have it) or weaken the claim.

### Question 2: Is the claim within the paper's scope?

A paper about post-discharge readmission for heart failure patients does not support a general claim about readmissions across all conditions. A paper from a single academic medical center does not support a claim about US healthcare broadly.

Specifically watch for:
- **Population overgeneralization** — extending findings from one population to a broader one.
- **Setting overgeneralization** — extending findings from one care setting to another.
- **Outcome overgeneralization** — extending findings on one outcome to a related but different one.
- **Time overgeneralization** — citing a paper from 2008 about EHR adoption to support a claim about EHR use today.

If the claim is broader than the paper, narrow the claim or find a better source.

### Question 3: Are effect sizes, populations, or settings being misrepresented?

This is the most common Gate 4 failure. The paper exists, the citation is correct, but the prose has subtly changed what the paper says.

- "Significantly reduced" → check the actual effect size and whether it is clinically meaningful, not just statistically significant.
- "Most patients" → check what fraction. "Most" is 51%+. Some papers use it for 65%, some for 90%. Use the number.
- "Recent study" → check the year. "Recent" in informatics is <5 years; in some specialties, <10. Be specific.
- "Large study" → check the sample size. Cite the n.

## The Three Failure Patterns

Pattern 1: **Drift across rewrites.** Prose was originally accurate. Over rewrites, the claim sharpened without anyone re-checking the source. The cited paper no longer supports the claim. Catch with a fresh Gate 4 pass before submission.

Pattern 2: **Strong claim, weak source.** A bold prose claim cites a small underpowered study or a single-center observational paper. The citation exists, but the evidence is thinner than the claim suggests. Either find better sources or weaken the claim to match.

Pattern 3: **Cargo-cult citation.** A citation that "everyone uses" for a claim, but when you actually read the paper, it does not say what everyone thinks it says. Common with often-cited papers that have become talismans rather than evidence. The Donabedian quality framework, the IOM "To Err Is Human" report, and the original burnout MBI papers are all victims of this — frequently cited for things they do not actually establish. Read the actual paper.

## The Protocol

When Gate 2 returns PASS:

1. **Read the abstract** the script returned. Skim if long, full read if the claim is load-bearing.
2. **Ask Question 1**: Is the claim in the abstract or obviously supported by it?
3. **Ask Question 2**: Is the claim within the paper's scope?
4. **Ask Question 3**: Are effect sizes / populations / settings represented accurately?
5. **If any answer is no**, decide:
   - Weaken the claim to match the source.
   - Find a better source.
   - Remove the claim.
6. **Log the result** in the citation log — note "abstract-only" vs "full-text-confirmed."

## When to Read Full Text vs Abstract

- **Abstract is sufficient** for: well-defined outcomes (mortality, readmission rates, costs), descriptive citations (citing a study's existence rather than its specific findings), background context.
- **Full text required** for: specific effect sizes, subgroup findings, methodology details, anything where the prose claim depends on a precise number.

If full text requires institutional access and is not available, mark the citation as "abstract-verified, full-text not reviewed" in the log. For peer-reviewed submissions, full-text review is the standard for any load-bearing citation.

## Gate 4 Failure Recovery

If a citation fails Gate 4:

1. The cited paper is real but doesn't support the claim → not a hallucination, but a misuse of evidence. The citation must change, or the claim must change.
2. Don't keep the citation while weakening the claim — if the paper genuinely supports the claim, keep the strong claim; if it doesn't, find a paper that does.
3. Log the failure. These failures, accumulated, signal places where the argument is reaching beyond the available evidence.

## The Operational Rule

Gate 4 is where most surviving errors get caught. A draft that has passed Gate 2 for every citation can still fail Gate 4 routinely. Build it into the writing loop, not the audit phase. Read the abstract when you add the citation, not when you submit.

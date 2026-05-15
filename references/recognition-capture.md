# Recognition Capture

The discipline this skill exists to protect.

## What Recognition Capture Is

**Recognition capture** is the moment you notice yourself — or the LLM writing alongside you — about to generate a confidence-based factual claim, identifier, statistic, or citation, and stop *before* committing it to prose.

Throughout this document, "you" refers to whoever is doing the writing. If you are using an LLM, the same recognition triggers apply to its output: you stop, the LLM stops, the placeholder goes in.

It is not a verification gate (those are Gates 1–5). It is the upstream practice that makes the gates work. A verification gate catches what was already written; recognition capture catches what was about to be written.

End-stage verification costs more than continuous verification because by the time the audit runs, the fabrication has already shaped the surrounding prose. The five gates move verification to inline. Recognition capture moves it earlier still — to the moment of *generation*, before the prose exists.

## Why This Step Exists

LLM training data contains many factually-correct statements paired with PMIDs, DOIs, author names, journals, years, effect sizes, and study populations. An LLM can produce highly confident output that combines these elements in plausible-but-wrong ways. The combinatorial nature of the failure is the problem: each individual element may be correct in its original context, but the specific combination the LLM generates is hallucinated.

The verification gates catch this after generation. Recognition capture catches it during generation, which is faster and produces a much smaller cleanup load.

## The Six Recognition Triggers

Six moments in writing where an LLM is most likely to confabulate. When any of these triggers fires, STOP and verify before continuing.

### Trigger 1: About to write an identifier (PMID, DOI, PMC ID)

When you (or your LLM) are about to write a specific identifier, ask:
- Did I retrieve this in the current session?
- Or do I "know" it from training data?

If the latter, STOP. Either:
- Search PubMed (via the PubMed MCP connector for Claude users, or via PubMed.gov for other tools) to retrieve the real identifier, or
- Write `[UNVERIFIED: identifier needed for claim about X]` and resolve before next paragraph

The "Class 4" failure mode (confident PMID resolving to a completely different paper) almost always begins here.

### Trigger 2: About to write a specific number, effect size, or population statistic

Examples of triggers:
- "30-day readmissions dropped by 22%..."
- "In a cohort of 2,847 patients..."
- "Mortality was 14.7% in the intervention group..."
- "Wait times decreased from 8.3 days to 4.1 days..."

When you (or your LLM) are about to write a precise number, ask:
- Have I seen this exact number in a verified source in this session?
- Or am I generating a plausible number?

Plausible numbers are the most dangerous form of fabrication because they pass casual review. STOP and either retrieve the actual number from a verified source or weaken the claim to qualitative language ("readmissions decreased meaningfully" rather than "by 22%").

### Trigger 3: About to write a study description ("A 2018 randomized trial showed...")

Examples:
- "A 2018 randomized trial demonstrated..."
- "In a recent JAMIA study..."
- "[A well-known author] and colleagues have shown..."
- "A multi-center cohort study found..."

When you (or your LLM) are about to describe a specific study, ask:
- Am I citing a specific paper I have a real PMID/DOI for?
- Or am I producing a generic-sounding description that pattern-matches what such a paper would say?

The latter is hallucinated study description. STOP. Either find the actual paper (and verify the description matches the abstract) or rewrite the claim to not require a specific study attribution.

### Trigger 4: About to write an author attribution

Examples:
- "[Senior author] and colleagues..."
- "As [a frequently-cited researcher] has argued..."
- "Following the framework proposed by Hoffman..."

When you (or your LLM) are about to attribute a position to a named author, ask:
- Do I have a specific verified source for this attribution?
- Or am I borrowing a well-known name from the field to anchor a general claim?

The latter is adjacent-author hallucination — the Class 2 signature documented in cross-disciplinary LLM citation studies. STOP. Either verify the attribution or rewrite without it.

### Trigger 5: About to write a date or temporal anchor

Examples:
- "In 2021..."
- "Since the 2009 HITECH Act..."
- "Recent CMS guidance..."

Specific dates need verification. "2021" sounds harmless until the cited finding was actually published in 2019 and the 2021 framing has shifted the temporal context of an argument. STOP and confirm dates against the source.

### Trigger 6: About to write "research has shown" / "studies suggest" without specific source

Examples:
- "Research has consistently shown..."
- "Multiple studies have demonstrated..."
- "The literature suggests..."

These framings are warning signs. They invite the reader to assume citations exist. When you are about to write one, ask:
- Do I have specific citations ready to support this in the next sentence?
- Or is this an unsupported general claim dressed in citation-implying language?

If the latter, STOP. Either provide the specific citations or remove the framing.

## The Capture Protocol

When any trigger fires:

1. **STOP generating the current sentence.** Do not finish it on momentum.
2. **Log the catch** in the Recognition Capture Log section of `citation_log.md`. Record: which trigger fired, what was about to be written, what resolution was applied.
3. **Apply one of three resolutions:**
   - **Retrieve**: Search PubMed, verify the identifier or claim, then write the sentence with verified content.
   - **Placeholder**: Write `[UNVERIFIED: brief description]` and resolve before the next paragraph.
   - **Rewrite**: Reformulate the sentence to not require the unverified element. (Example: "studies have shown a meaningful reduction" instead of "studies have shown a 22% reduction.")
4. **Resume writing** with the resolved sentence.

## Pattern Detection: Why the Log Matters

The Recognition Capture Log is not bureaucratic overhead. It is diagnostic.

Patterns that emerge over time:

- **Subfield clustering** — captures cluster in certain subfields (prior authorization, burnout research, EHR adoption). These are the subfields where LLM training data is densest and most prone to combinatorial fabrication.
- **Author-name clustering** — certain author names trigger captures more often because they appear in many adjacent papers.
- **Sentence-construction clustering** — sentences beginning "Recent work has shown..." or "[Senior author] and colleagues..." trigger captures disproportionately.
- **Time-of-session clustering** — captures often increase late in long writing sessions, when generation confidence rises and verification discipline drops.

The patterns are how the skill gets sharper over time. After enough sessions, patterns become visible to the writer: when writing about a heavily-published subfield, slow down; when citing a frequently-cited author, verify the specific paper; when the sentence wants to begin "Recent work...", check that the work is real before committing.

## Recognition Capture vs. Gate 2

These look similar but operate at different times:

| | Recognition Capture | Gate 2 |
|---|---|---|
| When | Before writing | After writing |
| What it watches | What is about to be generated | What was just generated |
| Mechanism | Self-monitoring during generation | Script verification of generated content |
| Output | Prevents fabrication entry into prose | Detects fabrication that entered prose |
| Cost | Zero (just stop and check) | Run script + reconcile |

Both run. Recognition capture catches the easy cases at the source. Gate 2 catches what slipped through. The Final Iterative Pass (Path B via MCP) is the safety net.

## How to Practice Recognition

Three habits that make recognition capture work:

1. **Slow generation on factual claims.** When the sentence is about to commit a specific number, name, date, or identifier, slow down. Speed of generation is correlated with fabrication risk.

2. **Read your own sentence before committing it.** Before writing the next sentence, re-read the one you just wrote. Did it commit a factual claim? Is that claim sourced? If not, fix it now, not later.

3. **Notice confidence as a signal, not a license.** When you feel confident about a specific PMID or effect size, that confidence is data — but not in the direction it feels. Confidence about a specific identifier that was not retrieved in the current session is the strongest signal that you should stop and verify, because confident-sounding wrong identifiers are the most damaging failure mode.

## The Operating Rule

If recognition capture is working, the Gate 2 verification load decreases over time. The verification gates are still mandatory, but they catch less because less is reaching them. The Recognition Capture Log will show this trend: fewer captures per session means recognition is becoming automatic. More captures means the discipline is finding things — also good, just an earlier stage.

A session with zero captures and many Gate 2 failures means recognition is not running. A session with many captures and zero Gate 2 failures means recognition is fully engaged. Aim for the second pattern.

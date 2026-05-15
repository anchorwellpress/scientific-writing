# Vancouver Citation Style

Vancouver is the numbered citation style used by PubMed-indexed journals across biomedical and health sciences fields. NLM (National Library of Medicine) maintains the canonical formatting at https://www.nlm.nih.gov/bsd/uniform_requirements.html.

## In-Text Citations

- Numbered in order of first appearance: ¹, ², ³, ...
- Superscript, no parentheses, placed **before** the period or comma: `...reduced 30-day readmissions.¹²`
- Multiple sequential citations: `...as prior work has shown.³⁻⁵`
- Multiple non-sequential: `...as several studies confirm.²,⁷,¹¹`
- Same source cited again → same number, do not assign a new one.
- Citation goes after the closing quotation mark but before the period: `"prior authorization is fundamentally a rationing tool."⁸`

## Reference List Format

At the end of the document, numbered in order of first appearance (not alphabetical). One reference per number.

### Journal Article (most common)

```
1. Author AA, Author BB, Author CC. Title of article in sentence case. Journal Abbreviation. Year;Volume(Issue):Pages. doi:10.xxxx/xxxxx
```

- Up to 6 authors listed; 7+ authors → first 6 then `, et al.`
- Author format: Last name + initials, no periods between initials, no spaces (e.g., `Smith JA`).
- Journal abbreviation per PubMed's NLM Catalog (e.g., `J Am Med Inform Assoc`, not `Journal of the American Medical Informatics Association`).
- Article title in sentence case (only first word + proper nouns capitalized).
- Year, volume, issue, pages — exact as PubMed lists.
- DOI is recommended, not always required. Include if available.

**Example:**
```
1. Smith JA, Jones BC, Doe DE. Title of the article in sentence case. J Example Med. 2024;15(3):200-210. doi:10.xxxx/example.2024.001
```

### Book

```
2. Author AA. Title of Book. Edition. Place of Publication: Publisher; Year.
```

**Example:**
```
2. Collins J. Good to Great: Why Some Companies Make the Leap and Others Don't. New York, NY: HarperBusiness; 2001.
```

### Book Chapter

```
3. Author AA, Author BB. Title of chapter. In: Editor AA, Editor BB, eds. Title of Book. Edition. Place: Publisher; Year:pages.
```

### Web Resource

```
4. Author or Organization. Title of page. Site Name. Published Date. Accessed Date. URL
```

**Example:**
```
4. Centers for Medicare & Medicaid Services. Interoperability and Prior Authorization Final Rule (CMS-0057-F). CMS.gov. Published January 17, 2024. Accessed May 15, 2026. https://www.cms.gov/...
```

### Preprint

```
5. Author AA, Author BB. Title of preprint. Server [Preprint]. Year. doi:10.xxxx/xxxxx
```

Mark explicitly as `[Preprint]`. Do not cite a preprint as if it were peer-reviewed.

## Common Formatting Errors

1. **Initials with periods**: Wrong: `Smith J.A.` Right: `Smith JA`
2. **Full journal name**: Wrong: `Journal of the American Medical Informatics Association`. Right: `J Am Med Inform Assoc`
3. **Title case in article title**: Wrong: `Toward Reliable Ascertainment of Evidence-Based Practices`. Right: `Toward reliable ascertainment of evidence-based practices`
4. **Spaces in DOI**: Wrong: `doi: 10.1093 / jamia / ocx083`. Right: `doi:10.1093/jamia/ocx083`
5. **Et al. without comma**: Wrong: `Author AA, Author BB et al.` Right: `Author AA, Author BB, et al.`
6. **Wrong author count threshold**: List up to 6, then et al. Some style guides say 3 — that is APA, not Vancouver.
7. **Alphabetical reference list**: Wrong for Vancouver. References must appear in citation order.

## Renumbering

When a citation is added in the middle of a draft, every subsequent number shifts. This is where errors creep in. Three options:

1. **Use the format_citation.py script** — preferred. Scans the document for `[Cite: PMID:XXXXX]` placeholders, assigns numbers in order of first appearance, generates the reference list. Run on demand.
2. **Manual renumbering with global find-replace** — error-prone but workable on short documents. Always re-audit afterwards with `audit_manuscript.py`.
3. **Author-year placeholders during drafting** (e.g., `(Smith 2018)`), converted to numbered Vancouver at the end. Acceptable for long-form pieces; risky for peer-reviewed submissions because the final conversion is its own error-prone step.

## Reference List Quality Check

Before submission, every entry should have:
- Complete author list (or 6 + et al.)
- Correct PubMed abbreviation for journal
- Year, volume, issue, pages
- DOI if available
- Sentence-case article title

A reference list with mixed formatting (some title-case titles, some sentence-case; some with DOI, some without when DOI exists) signals carelessness to reviewers. Format consistency matters.

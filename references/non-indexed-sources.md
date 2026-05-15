# Non-Indexed Sources

Sources that PubMed and Crossref don't cover, but that are legitimate and citable. The verification pipeline is different but the rigor is identical.

## What Counts as Non-Indexed

Common in health policy, clinical informatics, and health services research writing:

- **KFF (Kaiser Family Foundation)** — issue briefs, polling, Medicaid/Medicare data
- **Commonwealth Fund** — international comparison briefs, survey data
- **CMS regulatory documents** — final rules, transmittals, MLN Matters, CMS-0057-F type rules
- **Books** — Berwick's *Escape Fire*, Goldhill's *Catastrophic Care*, Collins' *Good to Great*
- **News investigative reporting** — STAT, ProPublica, Kaiser Health News (KHN, now KFF Health News)
- **Health Affairs Forefront** — blog format (distinct from peer-reviewed Health Affairs journal articles). Some Forefront posts are Crossref-indexed; many are not.
- **Think-tank papers** — Brookings, AEI, Urban Institute, Rand reports
- **Government data products** — MEPS, AHRQ databases, CDC WONDER
- **Industry reports** — Milliman, Mercer, Avalere
- **State agency reports** — California DHCS, OSHPD/HCAI data
- **Preprints not yet on indexed servers** — internal working papers from research groups

## The Non-Indexed Verification Protocol

For each non-indexed source:

### Step 1: Identify the Publisher Domain

The URL's domain tells you what level of verification is required.

- **High-trust publishers** (KFF, Commonwealth Fund, CMS.gov, federal .gov sites, established think tanks, major news organizations): publisher attestation is sufficient. The source exists where it says it does.
- **Medium-trust publishers** (consulting firms, state agencies, academic centers): verify the document is on the official site, not a third-party repost.
- **Low-trust or unfamiliar publishers**: additional verification required. Check the parent organization, the document's stated authorship, and cross-reference at least one specific claim from the document against another source.

### Step 2: Confirm URL Stability

Non-indexed sources move. URLs break. Two protections:

1. **Use the most stable URL form available.** For CMS, the rule's permanent URL (e.g., the federal register notice) is more stable than the CMS news release. For Health Affairs Forefront, the canonical post URL is more stable than a social media share link.
2. **Archive the page.** Submit the URL to `web.archive.org/save/[URL]` and record the resulting Wayback Machine URL in the log. This protects against link rot between draft and publication.

### Step 3: Record Access Date

Every non-indexed citation includes the date it was accessed in the Vancouver entry. Format:

```
Centers for Medicare & Medicaid Services. Interoperability and Prior Authorization Final Rule (CMS-0057-F). CMS.gov. Published January 17, 2024. Accessed May 15, 2026. https://www.cms.gov/...
```

The access date is what gives the citation its temporal anchor. Without it, a reader cannot reconstruct what the source said at the time of citing.

### Step 4: Verify the Specific Claim

Even more important than for indexed sources, because the "abstract" of a KFF brief is the executive summary, and the executive summary often softens specific findings. Read the methodology section. Verify the exact number being cited.

Common failure modes:
- KFF poll cited for "Americans support X" without specifying which subgroup. Read the crosstabs.
- CMS rule cited for "providers must do X by Y date" — verify the date and the specific provision; rules have multiple effective dates.
- Commonwealth Fund international comparison cited for "the US is worst at X" — verify which countries were in the comparison and which year.
- News investigative reporting cited for a specific finding — verify the finding is in the article body, not in a headline or pull quote.

### Step 5: Log the Citation

In the citation log, non-indexed sources include:
- Status: `non-indexed`
- Publisher domain
- Stable URL
- Wayback Machine URL (if archived)
- Access date
- Specific claim being supported
- Verification method (publisher attestation / cross-reference / methodology review)
- Gate 4 result (always required — read the actual content, not just the title)

## Vancouver Format for Non-Indexed Sources

### Government / Regulatory

```
Centers for Medicare & Medicaid Services. Interoperability and Prior Authorization Final Rule (CMS-0057-F). CMS.gov. Published January 17, 2024. Accessed May 15, 2026. https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-and-prior-authorization-final-rule-cms-0057-f
```

### Foundation Report

```
Kaiser Family Foundation. Health Insurance Coverage of the Total Population. KFF.org. Updated 2024. Accessed May 15, 2026. https://www.kff.org/other/state-indicator/total-population/
```

### Health Affairs Forefront Post

```
Author Last F. Title of post. Health Affairs Forefront. Published [date]. doi:10.1377/forefront.[ID] [if Crossref-indexed; if not, omit DOI and use URL]
```

### Book

```
Berwick DM, Nolan TW, Whittington J. The triple aim: care, health, and cost. Health Aff (Millwood). 2008;27(3):759-769. doi:10.1377/hlthaff.27.3.759
```
(For peer-reviewed Health Affairs articles, treat as indexed — they have DOIs.)

For trade books:
```
Goldhill D. Catastrophic Care: How American Health Care Killed My Father — and How We Can Fix It. New York, NY: Knopf; 2013.
```

### News Article

```
Author Last F. Title of article. STAT. Published [date]. Accessed [date]. URL
```

For investigative pieces:
```
Allen M, Pierce O. Medical errors are no. 3 cause of US deaths, researchers say. ProPublica. Published May 3, 2016. Accessed May 15, 2026. https://www.propublica.org/article/medical-errors-no-3-cause-of-us-deaths-researchers-say
```

### Preprint

```
Author Last F. Title of preprint. medRxiv [Preprint]. Published [date]. doi:10.1101/[ID]
```

Always include `[Preprint]` after the server name. Verify the preprint server's record before citing.

## When a Non-Indexed Source Becomes Questionable

Three signals that warrant skepticism:

1. **The source can't be found at the cited URL** and no archive copy exists. Treat as unverified.
2. **The source's publisher has changed positions or retracted** the document. Common for advocacy organizations. Check the current page.
3. **The cited claim isn't in the document at the cited URL** but is being attributed to the source. Cargo-cult citation in non-indexed form. Read the document; either find a better source or revise the claim.

## What Not to Cite

- Wikipedia (cite the underlying sources Wikipedia cites)
- Social media posts (even from credentialed authors; cite their underlying work)
- Press releases summarizing a study (cite the study)
- Conference abstracts unless explicitly marked `[Conference Abstract]` and used carefully — they often differ from the final paper
- Personal communication from a colleague — acceptable only with explicit permission and an in-text "(Personal communication, Name, Date)" marker, not in the reference list
- AI-generated content as a primary source. AI outputs are not citable evidence.

## The Operating Rule

Non-indexed verification is slower per citation than indexed verification. That is the price of citing a real source that the major indexes don't cover. The alternative — not citing the source — would weaken the argument or force a less appropriate substitute. Accept the slower pace; the citation is the source of credibility.

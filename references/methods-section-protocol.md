# Methods Section Protocol

For "Materials and Methods" sections in peer-reviewed journals, which have conventions beyond general scientific writing. Use after the main `peer-reviewed-register.md` and before drafting Methods.

## Structural Conventions

Most journals follow a predictable Methods section order. Deviating produces reviewer friction.

### Standard subsection sequence

1. **Study Design** — one paragraph framing the design type (cross-sectional, longitudinal, retrospective cohort, qualitative interview study, framework application, etc.) and the timeframe.
2. **Setting** — clinical site(s), system(s), data source(s). If multi-site, state the sites and any IRB-relevant identifiers. De-identify if required by data use agreement.
3. **Participants / Data Sources** — inclusion and exclusion criteria, with explicit counts at each filter step. For data sources: dataset name, version, date range, access mechanism.
4. **Variables / Measures** — what was measured or extracted. For each variable: definition, source, unit, coding logic.
5. **Statistical Analysis** — software (with version), tests used (with rationale for choice), handling of missing data, significance threshold, multiple-comparison correction if applicable.
6. **IRB / Ethics Statement** — IRB approval status, protocol number, consent waiver if applicable. For datasets that don't require IRB review, state why.
7. **Code and Data Availability** — most journals require this. State where code is deposited (GitHub URL with commit hash, or "available on request") and what data sharing is possible.

### Section header variations

Some journals use "Introduction" while others use "Background and Significance" as the second section header. Some use "Materials and Methods" while others use just "Methods." Check current author guidelines.

## Writing Conventions

### Active voice where possible

- "We extracted records for patients meeting inclusion criteria..." beats "Records were extracted..."
- "Two raters reviewed each case..." beats "Each case was reviewed by two raters..."

Methods sections traditionally use passive voice; most journals now accept both, and active is clearer.

### Specific over vague

- "Statistical analyses were performed using R version 4.3.1 (R Foundation for Statistical Computing)." Not "Standard statistical methods were used."
- "Inter-rater reliability was assessed using Fleiss' kappa for ≥3 raters." Not "Inter-rater reliability was calculated."
- "Patients were included if they had [specific criteria with codes and dates]." Not "Patients with [condition] were included."

### Cite every method

Methods choices need citations:
- Statistical methods → cite the original description or canonical textbook
- Framework being applied → cite the framework paper
- Validated instruments → cite the validation study
- Software → cite the software's reference

A Methods section with no citations is rare and usually wrong. A typical Methods section has 5–15 citations.

## Common Methods Patterns

### Retrospective Cohort from Administrative or Clinical Data

- **Data source format:** "[Data source name] (version [N]), accessed via [access mechanism] on [date range]."
- **Cohort identification:** list every filter, with counts at each step:
  - All eligible records in period: N
  - Filter 1 ([description]): N
  - Filter 2 ([description]): N
  - Final cohort: N
- **Comparator population:** state explicitly. If there's a relevant clinical or demographic stratification, name it.

### Qualitative or Mixed-Methods Work

- Sampling strategy (purposive, theoretical, convenience) with rationale
- Saturation criteria if claimed
- Coding approach (inductive, deductive, framework analysis)
- Number of coders and reliability assessment
- Software used for coding

### Framework Application / Methodology Papers

- The framework's original citation
- Specific adaptations made (with rationale)
- Application setting
- Reviewer panel size with reference to methodology recommendations
- Reliability assessment approach

`[CUSTOMIZE: Add your common Methods patterns here — the specific data sources, frameworks, or designs you use repeatedly. The more concrete the template, the faster Methods sections come together.]`

## Limitations: Substantive, Not Boilerplate

Every Methods-driven paper has limitations. The Limitations subsection (usually placed in Discussion, not Methods) should be substantive. Reviewer red flags:

- A limitations paragraph listing 6+ limitations with equal weight signals the author hasn't thought about which matter.
- Boilerplate ("single-center, retrospective, may not generalize") without specifics signals minimal thought.
- Strong substantive limitations include: known confounders not controlled for, measurement uncertainty in key variables, design choices that limit causal inference, sample size adequacy for the primary analysis.

## Code and Data Availability Statement

Most journals require this. Template options:

**Code available, data restricted:**
> "Analytic code is available at [GitHub URL, commit [hash]]. Patient-level data underlying this analysis cannot be shared due to the data use agreement with [data source]. Aggregated data are available from the corresponding author on reasonable request."

**Code and aggregated data available:**
> "Analytic code and aggregated data are available at [URL with commit hash or DOI]."

**Framework / methodology paper with no patient data:**
> "This methodology paper does not involve patient-level data. The framework and application materials are available at [URL]."

## Pre-Submission Checklist for Methods

- [ ] Setting and timeframe specified
- [ ] Inclusion/exclusion criteria with counts at each filter step
- [ ] Variables defined with source, unit, and coding
- [ ] Statistical software named with version
- [ ] Statistical tests named with rationale
- [ ] IRB / ethics statement included
- [ ] Code and data availability statement included
- [ ] Every method choice cited (5–15 citations typical)
- [ ] Limitations identified for the Discussion section
- [ ] AI use during Methods drafting logged in citation_log.md

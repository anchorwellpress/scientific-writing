#!/usr/bin/env python3
"""
verify_citation.py — Verify a citation against PubMed and Crossref.

Returns PASS / FLAG / FAIL based on:
  - Title fuzzy match
  - Author list match (the discriminator for adjacent-field hallucinations)
  - Journal match
  - Year match

Usage:
  python verify_citation.py --pmid 29346583
  python verify_citation.py --doi 10.1093/jamia/ocx083
  python verify_citation.py --reference "Embi PJ, Weiskopf NG, ..."
  python verify_citation.py --title "Toward reliable ascertainment" --author "Embi"
  python verify_citation.py --reference "..." --name-order family-first
  python verify_citation.py --preprint --doi 10.1101/2024.01.01.12345

Flags:
  --name-order family-first    For South Asian, Hungarian, East Asian names
                                where last token is the given name, not family
  --preprint                    Verify against preprint server (bioRxiv/medRxiv/arXiv)
                                rather than treating as peer-reviewed

Exit codes: 0 = PASS, 1 = FLAG, 2 = FAIL, 3 = network/parse error
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from difflib import SequenceMatcher

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CROSSREF_BASE = "https://api.crossref.org/works"
USER_AGENT = "scientific-writing-skill/1.1 (mailto:your-email@example.com)"
TIMEOUT = 15

PREPRINT_SERVERS = {
    "10.1101": "bioRxiv/medRxiv",
    "10.48550": "arXiv",
    "10.31219": "OSF Preprints",
    "10.21203": "Research Square",
    "10.20944": "Preprints.org",
}


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8")


def fuzzy_match(a, b, threshold=0.85):
    if not a or not b:
        return 0.0, False
    a_norm = re.sub(r"[^\w\s]", "", a.lower()).strip()
    b_norm = re.sub(r"[^\w\s]", "", b.lower()).strip()
    ratio = SequenceMatcher(None, a_norm, b_norm).ratio()
    return ratio, ratio >= threshold


def normalize_author(name, name_order="given-first"):
    """Extract last name from various formats.
    name_order: 'given-first' (Western default) or 'family-first' (some non-Western names)."""
    if not name:
        return ""
    name = name.strip()

    if "," in name:
        # "Family, Given" format — unambiguous regardless of name_order
        return name.split(",")[0].strip().lower()

    parts = name.split()
    if not parts:
        return ""

    # PubMed convention: "Family GivenInitials" (e.g., "Embi PJ")
    # Detect: last token is short and all caps → initials → previous is family name
    if len(parts) > 1 and re.match(r"^[A-Z]{1,4}\.?$", parts[-1]):
        return parts[-2].lower()

    # Otherwise depends on cultural convention
    if name_order == "family-first":
        # "Family Given" — first token is family name
        return parts[0].lower()
    else:
        # "Given Family" — last token is family name (Western default)
        return parts[-1].lower()


def parse_reference_string(ref, name_order="given-first"):
    """Best-effort parse of a Vancouver reference into components."""
    out = {"authors": [], "title": "", "journal": "", "year": ""}

    year_match = re.search(r"\b(19|20)\d{2}\b", ref)
    if year_match:
        out["year"] = year_match.group(0)

    parts = ref.split(". ", 2)
    if len(parts) >= 2:
        author_str = parts[0]
        author_str = re.sub(r",?\s*et al\.?", "", author_str)
        out["authors"] = [normalize_author(a, name_order) for a in author_str.split(",") if a.strip()]
    if len(parts) >= 2:
        out["title"] = parts[1].strip().rstrip(".")
    if len(parts) >= 3:
        rest = parts[2]
        journal_match = re.match(r"([^.\d]+?)(?:\.|\s+\d)", rest)
        if journal_match:
            out["journal"] = journal_match.group(1).strip()

    return out


def fetch_pubmed_by_pmid(pmid):
    url = f"{PUBMED_BASE}/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
    data = fetch_json(url)
    if "result" not in data or pmid not in data["result"]:
        return None
    rec = data["result"][pmid]
    if rec.get("error"):
        return None

    abstract = ""
    try:
        abstract_url = f"{PUBMED_BASE}/efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=text"
        abstract = fetch_text(abstract_url).strip()
    except Exception:
        pass

    return {
        "pmid": pmid,
        "title": rec.get("title", "").rstrip("."),
        "authors": [normalize_author(a.get("name", "")) for a in rec.get("authors", [])],
        "journal": rec.get("source", ""),
        "year": rec.get("pubdate", "")[:4],
        "volume": rec.get("volume", ""),
        "issue": rec.get("issue", ""),
        "pages": rec.get("pages", ""),
        "doi": next((aid.get("value") for aid in rec.get("articleids", []) if aid.get("idtype") == "doi"), ""),
        "abstract": abstract,
        "source": "PubMed",
    }


def fetch_pubmed_by_title(title, first_author=None):
    query = f'"{title}"[Title]'
    if first_author:
        query += f" AND {first_author}[Author]"
    url = f"{PUBMED_BASE}/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmode=json&retmax=5"
    data = fetch_json(url)
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_crossref_by_doi(doi):
    url = f"{CROSSREF_BASE}/{urllib.parse.quote(doi)}"
    try:
        data = fetch_json(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    msg = data.get("message", {})

    # Detect if this is a preprint
    doi_prefix = doi.split("/")[0] if "/" in doi else ""
    is_preprint = doi_prefix in PREPRINT_SERVERS or msg.get("type") == "posted-content"

    return {
        "doi": doi,
        "title": (msg.get("title") or [""])[0].rstrip("."),
        "authors": [normalize_author(f"{a.get('given','')} {a.get('family','')}") for a in msg.get("author", [])],
        "journal": (msg.get("container-title") or [""])[0] or PREPRINT_SERVERS.get(doi_prefix, "Preprint server"),
        "year": str((msg.get("issued", {}).get("date-parts") or [[""]])[0][0]),
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "pages": msg.get("page", ""),
        "abstract": msg.get("abstract", ""),
        "is_preprint": is_preprint,
        "source": "Crossref",
    }


def compare(claimed, fetched, name_order="given-first"):
    findings = []
    severity = 0

    if claimed.get("title"):
        ratio, ok = fuzzy_match(claimed["title"], fetched["title"])
        findings.append(f"Title match: {ratio:.2f} ({'OK' if ok else 'MISMATCH'})")
        if not ok:
            severity = max(severity, 1)

    if claimed.get("year"):
        if claimed["year"] != fetched["year"]:
            findings.append(f"Year MISMATCH: claimed {claimed['year']}, actual {fetched['year']}")
            severity = max(severity, 1)
        else:
            findings.append(f"Year match: {fetched['year']}")

    if claimed.get("journal"):
        ratio, ok = fuzzy_match(claimed["journal"], fetched["journal"], threshold=0.6)
        findings.append(f"Journal match: {ratio:.2f} ({'OK' if ok else 'MISMATCH'})")
        if not ok:
            severity = max(severity, 1)

    if claimed.get("authors"):
        claimed_authors = [a for a in claimed["authors"] if a]
        actual_authors = fetched.get("authors", [])

        if claimed_authors and actual_authors:
            if claimed_authors[0] != actual_authors[0]:
                findings.append(
                    f"FIRST AUTHOR MISMATCH: claimed '{claimed_authors[0]}', actual '{actual_authors[0]}' "
                    f"— classic Class 2 hallucination signature"
                )
                if name_order == "given-first":
                    findings.append(
                        f"  HINT: If author name is non-Western (South Asian, Hungarian, East Asian), "
                        f"re-run with --name-order family-first"
                    )
                severity = max(severity, 2)
            else:
                findings.append(f"First author match: {actual_authors[0]}")

        if claimed_authors and actual_authors:
            overlap = set(claimed_authors) & set(actual_authors)
            overlap_ratio = len(overlap) / max(len(claimed_authors), 1)
            findings.append(
                f"Author overlap: {len(overlap)}/{len(claimed_authors)} claimed authors found "
                f"({overlap_ratio:.0%})"
            )
            if overlap_ratio < 0.5:
                findings.append("AUTHOR LIST DIVERGENCE — likely Class 2 hallucination")
                severity = max(severity, 2)
            elif overlap_ratio < 1.0:
                severity = max(severity, 1)

    verdict = ["PASS", "FLAG", "FAIL"][severity]
    return verdict, findings


def main():
    parser = argparse.ArgumentParser(description="Verify a citation against PubMed/Crossref.")
    parser.add_argument("--pmid", help="PubMed ID")
    parser.add_argument("--doi", help="DOI")
    parser.add_argument("--reference", help="Full Vancouver reference string")
    parser.add_argument("--title", help="Article title (use with --author)")
    parser.add_argument("--author", help="First author last name (use with --title)")
    parser.add_argument("--name-order", choices=["given-first", "family-first"], default="given-first",
                        help="Cultural name order: given-first (Western default) or family-first (some non-Western)")
    parser.add_argument("--preprint", action="store_true", help="Treat citation as preprint (don't fail if no journal record)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if not (args.pmid or args.doi or args.reference or args.title):
        parser.error("Must provide --pmid, --doi, --reference, or --title")

    try:
        if args.pmid:
            fetched = fetch_pubmed_by_pmid(args.pmid)
            if not fetched:
                print(f"FAIL: PMID {args.pmid} not found in PubMed.")
                sys.exit(2)
            print(f"Found in PubMed:")
            print(f"  Title:   {fetched['title']}")
            print(f"  Authors: {', '.join(fetched['authors'][:6])}{' ...' if len(fetched['authors'])>6 else ''}")
            print(f"  Journal: {fetched['journal']} {fetched['year']};{fetched['volume']}({fetched['issue']}):{fetched['pages']}")
            print(f"  DOI:     {fetched['doi']}")
            print(f"\nVerdict: PASS (existence verified by PMID)")
            print(f"\n--- Abstract (read for Gate 4) ---")
            print(fetched['abstract'][:2000])
            if len(fetched['abstract']) > 2000:
                print(f"\n[... abstract truncated, full length {len(fetched['abstract'])} chars]")
            sys.exit(0)

        if args.doi:
            fetched = fetch_crossref_by_doi(args.doi)
            if not fetched:
                print(f"FAIL: DOI {args.doi} not found in Crossref.")
                sys.exit(2)

            if fetched.get("is_preprint") and not args.preprint:
                print(f"WARNING: DOI {args.doi} resolves to a preprint, not a peer-reviewed publication.")
                print(f"  Server: {fetched['journal']}")
                print(f"  Cite as [Preprint] in Vancouver. Re-run with --preprint to suppress this warning.")
                print()

            print(f"Found in Crossref:")
            print(f"  Title:   {fetched['title']}")
            print(f"  Authors: {', '.join(fetched['authors'][:6])}")
            print(f"  Journal: {fetched['journal']} {fetched['year']};{fetched['volume']}({fetched['issue']}):{fetched['pages']}")
            print(f"\nVerdict: PASS (existence verified by DOI)")
            sys.exit(0)

        if args.reference:
            claimed = parse_reference_string(args.reference, args.name_order)
            print(f"Parsed claim (name-order={args.name_order}):")
            print(f"  Title:   {claimed['title']}")
            print(f"  Authors: {claimed['authors']}")
            print(f"  Journal: {claimed['journal']}")
            print(f"  Year:    {claimed['year']}")
            print()

            first_author = claimed["authors"][0] if claimed["authors"] else None
            pmids = fetch_pubmed_by_title(claimed["title"], first_author)
            if not pmids:
                pmids = fetch_pubmed_by_title(claimed["title"])

            if not pmids:
                print(f"FAIL: No PubMed match for title '{claimed['title']}'.")
                print("Manual check: search Crossref, Google Scholar before concluding hallucination.")
                print("If source is non-indexed (KFF, CMS, book, news), use the non-indexed verification protocol instead.")
                sys.exit(2)

            fetched = fetch_pubmed_by_pmid(pmids[0])
            print(f"Best PubMed match (PMID {pmids[0]}):")
            print(f"  Title:   {fetched['title']}")
            print(f"  Authors: {', '.join(fetched['authors'][:6])}")
            print(f"  Journal: {fetched['journal']} {fetched['year']}")
            print()

            verdict, findings = compare(claimed, fetched, args.name_order)
            print(f"Verdict: {verdict}")
            print("\nFindings:")
            for f in findings:
                print(f"  - {f}")
            sys.exit({"PASS": 0, "FLAG": 1, "FAIL": 2}[verdict])

        if args.title:
            pmids = fetch_pubmed_by_title(args.title, args.author)
            if not pmids:
                print(f"FAIL: No PubMed match for '{args.title}'.")
                sys.exit(2)
            for pmid in pmids[:3]:
                rec = fetch_pubmed_by_pmid(pmid)
                if rec:
                    print(f"PMID {pmid}: {rec['title']} — {', '.join(rec['authors'][:3])}... {rec['journal']} {rec['year']}")
            sys.exit(0)

    except urllib.error.URLError as e:
        print(f"NETWORK ERROR: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"PARSE ERROR: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
format_citation.py — Convert PMID or DOI to a Vancouver-formatted reference entry.
Also handles renumbering of [Cite: PMID:XXXXX] placeholders in a manuscript,
scanning prose, tables, and figure legends for order-of-first-appearance.

Usage:
  python format_citation.py --pmid 29346583
  python format_citation.py --doi 10.1093/jamia/ocx083
  python format_citation.py --renumber manuscript.md
  python format_citation.py --renumber manuscript.md --out manuscript_renumbered.md
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CROSSREF_BASE = "https://api.crossref.org/works"
USER_AGENT = "scientific-writing-skill/1.1 (mailto:your-email@example.com)"
TIMEOUT = 15


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def format_author_vancouver(author_record):
    if "name" in author_record:
        return author_record["name"]
    if "family" in author_record:
        family = author_record.get("family", "")
        given = author_record.get("given", "")
        initials = "".join(part[0] for part in given.split() if part)
        return f"{family} {initials}".strip()
    return ""


def format_author_list(authors):
    if len(authors) <= 6:
        return ", ".join(authors)
    return ", ".join(authors[:6]) + ", et al."


def to_sentence_case(title):
    if not title:
        return ""
    title = title.strip().rstrip(".")
    if sum(1 for c in title if c.isupper()) > len(title) * 0.3:
        title = title[0].upper() + title[1:].lower()
        title = re.sub(r"(:\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), title)
    return title


def fetch_pmid(pmid):
    url = f"{PUBMED_BASE}/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
    data = fetch_json(url)
    rec = data.get("result", {}).get(pmid)
    if not rec or rec.get("error"):
        return None
    authors = [format_author_vancouver(a) for a in rec.get("authors", []) if a.get("authtype") == "Author"]
    doi = next((aid.get("value") for aid in rec.get("articleids", []) if aid.get("idtype") == "doi"), "")
    return {
        "authors": authors,
        "title": to_sentence_case(rec.get("title", "")),
        "journal": rec.get("source", ""),
        "year": rec.get("pubdate", "")[:4],
        "volume": rec.get("volume", ""),
        "issue": rec.get("issue", ""),
        "pages": rec.get("pages", ""),
        "doi": doi,
        "pmid": pmid,
    }


def fetch_doi(doi):
    url = f"{CROSSREF_BASE}/{urllib.parse.quote(doi)}"
    try:
        data = fetch_json(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    msg = data.get("message", {})
    authors = [format_author_vancouver(a) for a in msg.get("author", [])]
    return {
        "authors": authors,
        "title": to_sentence_case((msg.get("title") or [""])[0]),
        "journal": (msg.get("short-container-title") or msg.get("container-title") or [""])[0],
        "year": str((msg.get("issued", {}).get("date-parts") or [[""]])[0][0]),
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "pages": msg.get("page", ""),
        "doi": doi,
        "pmid": "",
    }


def format_vancouver(rec):
    authors = format_author_list(rec["authors"])
    title = rec["title"].rstrip(".")
    journal = rec["journal"]
    year = rec["year"]
    volume = rec["volume"]
    issue = rec["issue"]
    pages = rec["pages"]
    doi = rec.get("doi", "")

    citation = f"{authors}. {title}. {journal}. {year}"
    if volume:
        citation += f";{volume}"
    if issue:
        citation += f"({issue})"
    if pages:
        citation += f":{pages}"
    citation += "."
    if doi:
        citation += f" doi:{doi}"
    return citation


def renumber_manuscript(path, out_path=None):
    """Scan a manuscript for [Cite: PMID:XXXXX], [Cite: DOI:xxxx], and [Cite: NONINDEXED:label]
    placeholders across prose, tables, and figure legends. Number in absolute order of first
    appearance anywhere in the document (JAMIA rule), generate reference list."""
    with open(path) as f:
        text = f.read()

    # Patterns: [Cite: PMID:xxxx], [Cite: DOI:xxxx], [Cite: NONINDEXED:label]
    # NONINDEXED entries must be defined manually in a "Non-Indexed References" section
    pattern = re.compile(r"\[Cite:\s*(PMID|DOI|NONINDEXED):\s*([^\]]+)\]", re.IGNORECASE)
    matches = list(pattern.finditer(text))

    if not matches:
        print(f"No [Cite: PMID:...], [Cite: DOI:...], or [Cite: NONINDEXED:...] placeholders found in {path}.")
        return

    # Order of first appearance — absolute, including tables and figure legends
    # (no special handling needed; the linear scan captures absolute order)
    order = {}
    locations = {}  # for reporting: where each citation first appeared
    for m in matches:
        key = (m.group(1).upper(), m.group(2).strip())
        if key not in order:
            order[key] = len(order) + 1
            # Find what section the first appearance is in
            preceding_text = text[:m.start()]
            # Locate the most recent heading
            heading_match = list(re.finditer(r"^#{1,4}\s+(.+)$", preceding_text, re.MULTILINE))
            section = heading_match[-1].group(1) if heading_match else "(before first heading)"
            # Detect table or figure context
            context = ""
            tail = preceding_text[-200:]
            if re.search(r"^\|", tail, re.MULTILINE) or "Table" in tail[-100:]:
                context = " [in table]"
            elif "Figure" in tail[-100:] or "Fig." in tail[-100:]:
                context = " [in figure legend]"
            locations[key] = f"{section}{context}"

    def replace(m):
        key = (m.group(1).upper(), m.group(2).strip())
        return f"<sup>{order[key]}</sup>"

    new_text = pattern.sub(replace, text)

    # Look for a manually-defined "Non-Indexed References" section to pull NONINDEXED entries
    nonindexed_section = re.search(
        r"#{1,4}\s+Non-?Indexed References?\s*\n(.+?)(?=\n#{1,4}\s|\Z)",
        text, re.DOTALL | re.IGNORECASE
    )
    nonindexed_entries = {}
    if nonindexed_section:
        for line in nonindexed_section.group(1).split("\n"):
            # Format: "label: full Vancouver-style non-indexed reference"
            m = re.match(r"^\s*([A-Za-z0-9_-]+)\s*:\s*(.+)$", line)
            if m:
                nonindexed_entries[m.group(1).strip().upper()] = m.group(2).strip()

    # Generate reference list
    refs = ["", "", "## References", ""]
    for (id_type, identifier), num in sorted(order.items(), key=lambda x: x[1]):
        try:
            if id_type == "PMID":
                rec = fetch_pmid(identifier)
                entry = format_vancouver(rec) if rec else f"[UNRESOLVED PMID: {identifier}]"
            elif id_type == "DOI":
                rec = fetch_doi(identifier)
                entry = format_vancouver(rec) if rec else f"[UNRESOLVED DOI: {identifier}]"
            elif id_type == "NONINDEXED":
                entry = nonindexed_entries.get(identifier.upper(),
                    f"[NON-INDEXED reference '{identifier}' not defined in Non-Indexed References section]")
            else:
                entry = f"[UNKNOWN id type: {id_type}]"
            refs.append(f"{num}. {entry}")
        except Exception as e:
            refs.append(f"{num}. [ERROR resolving {id_type}: {identifier} — {e}]")

    new_text = new_text.rstrip() + "\n" + "\n".join(refs) + "\n"

    output = out_path or path.replace(".md", "_renumbered.md")
    with open(output, "w") as f:
        f.write(new_text)
    print(f"Renumbered manuscript written to: {output}")
    print(f"Resolved {len(order)} unique citations.")
    print("\nCitation order of first appearance:")
    for (id_type, identifier), num in sorted(order.items(), key=lambda x: x[1]):
        print(f"  {num}. {id_type}:{identifier} (first appearance: {locations.get((id_type, identifier), '?')})")


def main():
    parser = argparse.ArgumentParser(description="Format Vancouver citations from PMID/DOI; renumber manuscripts.")
    parser.add_argument("--pmid", help="PubMed ID")
    parser.add_argument("--doi", help="DOI")
    parser.add_argument("--renumber", help="Manuscript file with [Cite: PMID:xxxx] placeholders")
    parser.add_argument("--out", help="Output path for renumbered manuscript")
    args = parser.parse_args()

    if args.pmid:
        rec = fetch_pmid(args.pmid)
        if not rec:
            print(f"PMID {args.pmid} not found.", file=sys.stderr)
            sys.exit(1)
        print(format_vancouver(rec))
    elif args.doi:
        rec = fetch_doi(args.doi)
        if not rec:
            print(f"DOI {args.doi} not found.", file=sys.stderr)
            sys.exit(1)
        print(format_vancouver(rec))
    elif args.renumber:
        renumber_manuscript(args.renumber, args.out)
    else:
        parser.error("Provide --pmid, --doi, or --renumber")


if __name__ == "__main__":
    main()

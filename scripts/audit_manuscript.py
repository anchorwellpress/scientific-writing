#!/usr/bin/env python3
"""
audit_manuscript.py — Audit every citation in a manuscript.

Scans for:
  - [Cite: PMID:XXXXX] placeholders → verifies each PMID
  - [Cite: DOI:xxxx] placeholders → verifies each DOI
  - [Cite: NONINDEXED:label] placeholders → flags for manual confirmation
  - Numbered references in a "References" section → verifies by reference string
  - [UNVERIFIED: ...] markers → flagged for resolution

Modes:
  Default audit             python audit_manuscript.py manuscript.md
  With report file          python audit_manuscript.py manuscript.md --report report.md
  Diff-aware revision audit python audit_manuscript.py --diff old.md new.md
  Self-citation check       python audit_manuscript.py manuscript.md --self-citation-check --author "Smith"
  Word-count check          python audit_manuscript.py manuscript.md --word-count --limit 3500
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
VERIFY_SCRIPT = SCRIPT_DIR / "verify_citation.py"


def find_placeholders(text):
    """Find [Cite: PMID:xxxx], [Cite: DOI:xxxx], [Cite: NONINDEXED:label] placeholders."""
    pattern = re.compile(r"\[Cite:\s*(PMID|DOI|NONINDEXED):\s*([^\]]+)\]", re.IGNORECASE)
    return [(m.group(1).upper(), m.group(2).strip()) for m in pattern.finditer(text)]


def find_unverified(text):
    """Find [UNVERIFIED: ...] placeholders inside prose body.

    Excludes occurrences inside sections titled 'AI Use Disclosure', 'Submission Status',
    'Notes', 'AI Use', or 'Recognition Capture Log', and inside fenced code blocks."""
    # Strip fenced code blocks first
    body = re.sub(r"```.+?```", "", text, flags=re.DOTALL)
    # Split into sections by heading, exclude meta sections
    excluded_titles = re.compile(
        r"^(AI Use Disclosure|Submission Status|Notes for|AI Use|Recognition Capture Log)",
        re.IGNORECASE,
    )
    sections = re.split(r"(?=^#{1,4}\s+)", body, flags=re.MULTILINE)
    kept = []
    for section in sections:
        heading_match = re.match(r"^#{1,4}\s+(.+?)$", section, re.MULTILINE)
        if heading_match and excluded_titles.match(heading_match.group(1).strip()):
            continue
        kept.append(section)
    prose_only = "\n".join(kept)
    return re.findall(r"\[UNVERIFIED:[^\]]*\]", prose_only)


def find_reference_list(text):
    """Find a 'References' section and extract numbered entries.
    Handles both '## References' and '# References' headers."""
    match = re.search(r"(?:^|\n)#{1,3}\s*References?\s*\n(.+?)(?=\n#{1,3}\s|\Z)", text, re.DOTALL | re.IGNORECASE)
    if not match:
        return []
    ref_block = match.group(1)
    entries = re.findall(r"^\s*(\d+)\.\s*(.+?)(?=\n\s*\d+\.\s|\Z)", ref_block, re.MULTILINE | re.DOTALL)
    return [(int(num), ref.strip().replace("\n", " ")) for num, ref in entries]


def find_inline_numbered_citations(text):
    """Find inline numbered citations like ^1, ^1,2,3, ^1-3, <sup>1</sup>."""
    citations = []
    # Match superscript numbers in HTML or markdown
    pattern = re.compile(r"<sup>(\d+(?:[,\-]\d+)*)</sup>")
    for m in pattern.finditer(text):
        citations.append(m.group(1))
    return citations


def count_body_words(text):
    """Count body text words, excluding title, abstract, references, tables, figure legends, ack."""
    # Remove reference section
    text = re.sub(r"(?:^|\n)#{1,3}\s*References?\s*\n.+?(?=\n#{1,3}\s|\Z)", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Remove abstract section
    text = re.sub(r"(?:^|\n)#{1,3}\s*Abstract\s*\n.+?(?=\n#{1,3}\s|\Z)", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Remove acknowledgments
    text = re.sub(r"(?:^|\n)#{1,3}\s*Acknowledg[em]ents?\s*\n.+?(?=\n#{1,3}\s|\Z)", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Remove tables (markdown table lines)
    text = re.sub(r"^\|.*$", "", text, flags=re.MULTILINE)
    # Remove figure legend blocks (heuristic: lines starting with "Figure" or "Fig.")
    text = re.sub(r"^(Figure|Fig\.)\s+\d+.*$", "", text, flags=re.MULTILINE)
    # Remove first-line title (heuristic: first level-1 heading)
    text = re.sub(r"\A\s*#\s+.+?\n", "", text, count=1)
    # Remove headings themselves
    text = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE)
    # Remove placeholders so they don't count as words
    text = re.sub(r"\[Cite:[^\]]+\]", "", text)
    text = re.sub(r"<sup>[^<]+</sup>", "", text)
    # Count words
    words = re.findall(r"\S+", text)
    return len(words)


def run_verify(args):
    try:
        result = subprocess.run(
            [sys.executable, str(VERIFY_SCRIPT)] + args,
            capture_output=True, text=True, timeout=30,
        )
        verdict = {0: "PASS", 1: "FLAG", 2: "FAIL", 3: "ERROR"}.get(result.returncode, "UNKNOWN")
        return verdict, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "ERROR", "Timeout"
    except Exception as e:
        return "ERROR", str(e)


def audit(manuscript_path, report_path=None):
    text = Path(manuscript_path).read_text()

    placeholders = find_placeholders(text)
    unverified = find_unverified(text)
    refs = find_reference_list(text)
    inline_nums = find_inline_numbered_citations(text)

    results = []
    summary = {"PASS": 0, "FLAG": 0, "FAIL": 0, "ERROR": 0,
               "UNVERIFIED": len(unverified), "NONINDEXED_MANUAL": 0}

    print(f"Found {len(placeholders)} [Cite:] placeholders, "
          f"{len(refs)} numbered references in reference list, "
          f"{len(inline_nums)} inline numbered citations, "
          f"{len(unverified)} [UNVERIFIED] markers.\n")

    # Co-author draft detection
    if refs and not placeholders:
        print("NOTE: Document uses pre-numbered Vancouver references without [Cite:] placeholders.")
        print("Likely a co-author draft or post-renumber state. Auditing reference list directly.\n")

    seen = set()
    # Audit placeholders
    for id_type, identifier in placeholders:
        key = (id_type, identifier)
        if key in seen:
            continue
        seen.add(key)
        if id_type == "NONINDEXED":
            print(f"  [NONINDEXED_MANUAL] {identifier} — requires manual verification per non-indexed-sources.md")
            summary["NONINDEXED_MANUAL"] += 1
            results.append({"type": "noninexed", "identifier": identifier, "verdict": "MANUAL", "output": "Requires manual verification."})
            continue
        arg = "--pmid" if id_type == "PMID" else "--doi"
        verdict, output = run_verify([arg, identifier])
        summary[verdict if verdict in summary else "ERROR"] += 1
        results.append({"type": "placeholder", "identifier": f"{id_type}:{identifier}", "verdict": verdict, "output": output[:500]})
        print(f"  [{verdict}] {id_type}:{identifier}")

    # Audit reference list entries
    for num, ref in refs:
        verdict, output = run_verify(["--reference", ref])
        summary[verdict if verdict in summary else "ERROR"] += 1
        results.append({"type": "reference", "identifier": f"Ref {num}: {ref[:80]}...", "verdict": verdict, "output": output[:500]})
        print(f"  [{verdict}] Ref {num}: {ref[:60]}...")

    # Numbering integrity: does every number in body appear in reference list?
    if refs and inline_nums:
        body_numbers = set()
        for c in inline_nums:
            # Handle "1,2,3" or "1-3" forms
            for part in c.split(","):
                if "-" in part:
                    start, end = part.split("-")
                    body_numbers.update(range(int(start), int(end) + 1))
                else:
                    body_numbers.add(int(part))
        ref_numbers = set(num for num, _ in refs)
        in_body_not_in_refs = body_numbers - ref_numbers
        in_refs_not_in_body = ref_numbers - body_numbers
        if in_body_not_in_refs:
            print(f"\n⚠ Body cites numbers not in reference list: {sorted(in_body_not_in_refs)}")
            summary["FAIL"] += len(in_body_not_in_refs)
        if in_refs_not_in_body:
            print(f"⚠ Reference list contains numbers not cited in body: {sorted(in_refs_not_in_body)}")
            summary["FLAG"] += len(in_refs_not_in_body)

    print("\n=== SUMMARY ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    fail_count = summary["FAIL"] + summary["ERROR"]
    if fail_count > 0 or summary["UNVERIFIED"] > 0 or summary["NONINDEXED_MANUAL"] > 0:
        print(f"\n⚠ {fail_count} failed verification, {summary['UNVERIFIED']} unverified markers, "
              f"{summary['NONINDEXED_MANUAL']} non-indexed citations need manual confirmation.")
        print("Manuscript is NOT ready for submission.")
    elif summary["FLAG"] > 0:
        print(f"\n⚠ {summary['FLAG']} flagged — manual review required before submission.")
    else:
        print("\n✓ All citations verified.")

    if report_path:
        lines = [f"# Citation Audit Report\n", f"**Manuscript:** {manuscript_path}\n", "## Summary\n"]
        for k, v in summary.items():
            lines.append(f"- {k}: {v}")
        lines.append("\n## Per-Citation Results\n")
        for r in results:
            lines.append(f"### [{r['verdict']}] {r['identifier']}\n")
            lines.append("```")
            lines.append(r['output'])
            lines.append("```\n")
        if unverified:
            lines.append("\n## Unverified Markers\n")
            for u in unverified:
                lines.append(f"- {u}")
        Path(report_path).write_text("\n".join(lines))
        print(f"\nFull report: {report_path}")


def diff_audit(old_path, new_path):
    """Compare two manuscript versions, audit only what changed."""
    old_text = Path(old_path).read_text()
    new_text = Path(new_path).read_text()

    old_cites = set(find_placeholders(old_text))
    new_cites = set(find_placeholders(new_text))

    added = new_cites - old_cites
    removed = old_cites - new_cites
    unchanged = old_cites & new_cites

    print(f"=== DIFF-AWARE AUDIT ===")
    print(f"Old: {old_path} ({len(old_cites)} unique citations)")
    print(f"New: {new_path} ({len(new_cites)} unique citations)")
    print(f"\nAdded:     {len(added)}")
    print(f"Removed:   {len(removed)}")
    print(f"Unchanged: {len(unchanged)}")

    if added:
        print("\n=== Newly added citations (require Gate 2 + Gate 4) ===")
        for id_type, identifier in sorted(added):
            if id_type == "NONINDEXED":
                print(f"  NONINDEXED:{identifier} — manual verification required")
                continue
            arg = "--pmid" if id_type == "PMID" else "--doi"
            verdict, _ = run_verify([arg, identifier])
            print(f"  [{verdict}] {id_type}:{identifier}")

    if removed:
        print("\n=== Removed citations (mark RETIRED in log) ===")
        for id_type, identifier in sorted(removed):
            print(f"  {id_type}:{identifier}")

    if unchanged:
        print(f"\n=== Unchanged citations: {len(unchanged)} (re-verify only if claim changed) ===")
        print("  Manually check whether the prose claim attached to each unchanged citation has been sharpened.")
        print("  If so, re-walk Gate 4 for that citation in the new version.")


def self_citation_check(manuscript_path, author_name):
    """Flag potential self-citation creep."""
    text = Path(manuscript_path).read_text()
    refs = find_reference_list(text)

    if not refs:
        print("No reference list found. Run after renumbering.")
        return

    author_lower = author_name.lower()
    self_cites = []
    for num, ref in refs:
        # Check if author appears in the first ~150 chars (author list)
        if author_lower in ref[:200].lower():
            self_cites.append((num, ref))

    total = len(refs)
    n_self = len(self_cites)
    ratio = n_self / total if total else 0

    print(f"=== SELF-CITATION CHECK ===")
    print(f"Author: {author_name}")
    print(f"Total citations: {total}")
    print(f"Self-citations: {n_self} ({ratio:.0%})")

    if ratio > 0.20:
        print(f"\n⚠ Self-citation ratio exceeds 20% threshold. Review for self-citation creep.")
    else:
        print(f"\n✓ Self-citation ratio within typical range.")

    if self_cites:
        print(f"\nSelf-cited references:")
        for num, ref in self_cites:
            print(f"  {num}. {ref[:120]}...")

    # Discussion-section anchor check
    discussion_match = re.search(r"(?:^|\n)#{1,3}\s*Discussion\s*\n(.+?)(?=\n#{1,3}\s|\Z)", text, re.DOTALL | re.IGNORECASE)
    if discussion_match:
        disc_text = discussion_match.group(1)
        disc_nums = set()
        for c in find_inline_numbered_citations(disc_text):
            for part in c.split(","):
                if "-" in part:
                    start, end = part.split("-")
                    disc_nums.update(range(int(start), int(end) + 1))
                else:
                    disc_nums.add(int(part))
        disc_self = sum(1 for num, _ in self_cites if num in disc_nums)
        if disc_nums:
            disc_ratio = disc_self / len(disc_nums)
            print(f"\nDiscussion section: {disc_self}/{len(disc_nums)} citations are self-cites ({disc_ratio:.0%})")
            if disc_ratio > 0.30:
                print(f"  ⚠ Discussion section appears anchored on prior author work. Consider broader evidence base.")


def word_count_check(manuscript_path, limit):
    text = Path(manuscript_path).read_text()
    n = count_body_words(text)
    print(f"=== WORD COUNT ===")
    print(f"Manuscript: {manuscript_path}")
    print(f"Body word count (excludes title, abstract, references, tables, figure legends, acknowledgments): {n}")
    if limit:
        if n > limit:
            print(f"⚠ Over limit by {n - limit} words (limit: {limit})")
        elif n > limit * 0.95:
            print(f"⚠ Near limit ({n}/{limit}) — tighten before submission")
        else:
            print(f"✓ Under limit ({n}/{limit})")


def main():
    parser = argparse.ArgumentParser(description="Audit citations in a manuscript.")
    parser.add_argument("manuscript", nargs="?", help="Path to manuscript")
    parser.add_argument("--report", help="Write detailed audit report")
    parser.add_argument("--diff", nargs=2, metavar=("OLD", "NEW"),
                        help="Diff-aware revision audit between two manuscript versions")
    parser.add_argument("--self-citation-check", action="store_true",
                        help="Run self-citation analysis (requires --author)")
    parser.add_argument("--author", help="Author last name for self-citation check")
    parser.add_argument("--word-count", action="store_true", help="Run word-count check")
    parser.add_argument("--limit", type=int, help="Word-count limit for check")
    args = parser.parse_args()

    if args.diff:
        diff_audit(args.diff[0], args.diff[1])
    elif args.self_citation_check:
        if not (args.manuscript and args.author):
            parser.error("--self-citation-check requires manuscript path and --author")
        self_citation_check(args.manuscript, args.author)
    elif args.word_count:
        if not args.manuscript:
            parser.error("--word-count requires manuscript path")
        word_count_check(args.manuscript, args.limit)
    elif args.manuscript:
        audit(args.manuscript, args.report)
    else:
        parser.error("Provide manuscript path or --diff OLD NEW")


if __name__ == "__main__":
    main()

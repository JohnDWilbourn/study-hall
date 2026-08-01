"""
audit_scripture_index.py
Finds ESV scripture references in doctrine pages missing from scripture-index.html.
Run from the doctrines folder.
"""

from pathlib import Path
import re

SKIP_FILES = {
    "doctrine-library.html",
    "scripture-index.html",
    "index.html",
    "20260801_001_split_doctrines.py",
    "20260801_002_doctrine-library.html",
    "split_doctrines.py",
    "add_doctrine_buttons.py",
    "fix_image_download.py",
    "audit_scripture_index.py",
}

def extract_esv_refs(content):
    """Extract all ESV.org URLs from HTML content."""
    return set(re.findall(r'href="(https://www\.esv\.org/[^"]+)"', content))

def main():
    # Load scripture index
    index_path = Path("scripture-index.html")
    index_content = index_path.read_text(encoding="utf-8")
    index_refs = extract_esv_refs(index_content)
    print(f"Scripture index has {len(index_refs)} ESV references.")

    # Load all doctrine pages
    doctrine_files = [f for f in Path(".").glob("*.html") if f.name not in SKIP_FILES]
    print(f"Scanning {len(doctrine_files)} doctrine pages...\n")

    all_doctrine_refs = {}  # ref -> set of doctrine filenames
    for f in sorted(doctrine_files):
        content = f.read_text(encoding="utf-8")
        refs = extract_esv_refs(content)
        for ref in refs:
            if ref not in all_doctrine_refs:
                all_doctrine_refs[ref] = set()
            all_doctrine_refs[ref].add(f.name)

    print(f"Doctrine pages contain {len(all_doctrine_refs)} unique ESV references.")

    # Find missing
    missing = {ref: doctrines for ref, doctrines in all_doctrine_refs.items()
               if ref not in index_refs}

    print(f"\nMISSING from scripture index: {len(missing)} references\n")
    print(f"{'Reference URL':<70} {'Doctrine(s)'}")
    print("-" * 120)
    for ref in sorted(missing.keys()):
        doctrines = ", ".join(sorted(missing[ref]))
        # Clean up URL for display
        display = ref.replace("https://www.esv.org/", "").replace("+", " ")
        print(f"{display:<70} {doctrines}")

    # Write missing refs to a file for further processing
    out = Path("missing_scripture_refs.txt")
    with out.open("w", encoding="utf-8") as f:
        f.write(f"Missing scripture references: {len(missing)}\n\n")
        for ref in sorted(missing.keys()):
            doctrines = ", ".join(sorted(missing[ref]))
            display = ref.replace("https://www.esv.org/", "").replace("+", " ")
            f.write(f"{display}\t{ref}\t{doctrines}\n")
    print(f"\nFull list written to: {out}")

if __name__ == "__main__":
    main()

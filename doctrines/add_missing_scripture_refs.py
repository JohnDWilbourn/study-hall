"""
add_missing_scripture_refs.py
Adds missing ESV references to scripture-index.html from missing_scripture_refs.txt.
Run from the doctrines folder.
"""

from pathlib import Path
import re

# Book order for sorting
BOOK_ORDER = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
    "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
    "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
    "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
    "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
    "Jude", "Revelation"
]

BOOK_INDEX = {b: i for i, b in enumerate(BOOK_ORDER)}

# Abbreviated book name normalization
ABBREV_MAP = {
    "Gen": "Genesis", "Exo": "Exodus", "Lev": "Leviticus",
    "Num": "Numbers", "Deut": "Deuteronomy", "Josh": "Joshua",
    "Judg": "Judges", "1 Sam": "1 Samuel", "2 Sam": "2 Samuel",
    "1 Kgs": "1 Kings", "2 Kgs": "2 Kings", "Neh": "Nehemiah",
    "Isa": "Isaiah", "Jer": "Jeremiah", "Ezek": "Ezekiel",
    "Dan": "Daniel", "Hos": "Hosea", "Zeph": "Zephaniah",
    "Hab": "Habakkuk", "Zech": "Zechariah", "Mal": "Malachi",
    "Matt": "Matthew", "Mk": "Mark", "Lk": "Luke",
    "Jn": "John", "Rom": "Romans",
    "1 Cor": "1 Corinthians", "2 Cor": "2 Corinthians",
    "Gal": "Galatians", "Eph": "Ephesians", "Phil": "Philippians",
    "Col": "Colossians", "1 Thess": "1 Thessalonians",
    "2 Thess": "2 Thessalonians", "1 Tim": "1 Timothy",
    "2 Tim": "2 Timothy", "Heb": "Hebrews", "Jas": "James",
    "1 Pet": "1 Peter", "2 Pet": "2 Peter", "Rev": "Revelation",
    "Prov": "Proverbs", "Ps": "Psalms", "Psa": "Psalms",
    "Hab": "Habakkuk", "Amos": "Amos", "Joel": "Joel",
    "Jude": "Jude", "Acts": "Acts",
}

SKIP_REFS = {
    "Rev 7:14\u2014cleansed by faith, represented as blood"
}

def normalize_book(ref_display):
    """Extract and normalize book name from display reference."""
    parts = ref_display.strip().split()
    # Handle numbered books
    if parts[0] in ("1", "2", "3") and len(parts) > 1:
        abbrev = parts[0] + " " + parts[1]
        rest = " ".join(parts[2:])
    else:
        abbrev = parts[0]
        rest = " ".join(parts[1:])

    full = ABBREV_MAP.get(abbrev, abbrev)
    return full, rest

def build_table_row(display_ref, esv_url, doctrine_links):
    """Build an HTML table row for a scripture reference."""
    book, verse = normalize_book(display_ref)
    doctrine_html = ", ".join(
        f'<a href="{slug}">{slug.replace(".html","").replace("-"," ").title()}</a>'
        for slug in sorted(doctrine_links)
    )
    return (
        book,
        f'        <tr>\n'
        f'            <td>{book}</td>\n'
        f'            <td><a href="{esv_url}" target="_blank">{verse.strip()}</a></td>\n'
        f'            <td><span class="hover-cue">— hover reference to preview</span></td>\n'
        f'            <td>{doctrine_html}</td>\n'
        f'        </tr>\n'
    )

def main():
    missing_file = Path("missing_scripture_refs.txt")
    if not missing_file.exists():
        print("Run audit_scripture_index.py first to generate missing_scripture_refs.txt")
        return

    # Parse missing refs
    entries = []
    with missing_file.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("Missing"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            display, url, doctrines_str = parts[0], parts[1], parts[2]
            if display in SKIP_REFS:
                print(f"  SKIP (malformed): {display}")
                continue
            doctrine_slugs = [d.strip() for d in doctrines_str.split(",")]
            entries.append((display, url, doctrine_slugs))

    print(f"Loaded {len(entries)} missing references to add.")

    # Load scripture index
    index_path = Path("scripture-index.html")
    content = index_path.read_text(encoding="utf-8")

    # Build new rows grouped by book
    added = 0
    for display, url, doctrine_slugs in entries:
        book, verse = normalize_book(display)
        _, row_html = build_table_row(display, url, doctrine_slugs)

        # Find insertion point — after last row for this book, or before next book
        # Simple approach: insert before </tbody>
        content = content.replace("</tbody>", row_html + "        </tbody>", 1)
        added += 1

    index_path.write_text(content, encoding="utf-8")
    print(f"Added {added} rows to scripture-index.html.")
    print("NOTE: Rows are appended before </tbody> — you may want to re-sort by book order.")
    print("The existing sort/filter JS will still work correctly.")

if __name__ == "__main__":
    main()

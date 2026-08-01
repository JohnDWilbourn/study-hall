"""
split_doctrines.py
Splits doctrine-library.html into individual doctrine pages.
Run from the doctrines folder
"""

from pathlib import Path
from bs4 import BeautifulSoup
import re

SOURCE = Path("doctrine-library.html")
OUT_DIR = Path(".")

# ── Shared CSS extracted from doctrine-library.html ──────────────────────────
HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Library of Christian Doctrines</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Cinzel:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --parchment: #f4ecd8;
  --ink: #2a2118;
  --gold: #b8973a;
  --gold-dim: #8a7129;
  --border: #d9cba8;
  --ink-soft: #3a2e1a;
  --section-bg: #fdfbf5;
  --code-bg: #ede2c6;
}}
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ scroll-behavior: smooth; }}
body {{
  background: var(--parchment);
  color: var(--ink);
  font-family: 'EB Garamond', serif;
  font-size: 1.05rem;
  line-height: 1.75;
  padding: 0;
}}
.site-header {{
  background: var(--ink);
  color: var(--parchment);
  padding: 2rem 1.5rem 1.5rem;
  text-align: center;
  border-bottom: 3px solid var(--gold);
}}
.site-header h1 {{
  font-family: 'Cinzel', serif;
  font-size: 2rem;
  font-weight: 700;
  color: var(--parchment);
  letter-spacing: 0.04em;
  margin-bottom: 0.25rem;
}}
.site-header .subtitle {{
  font-size: 0.95rem;
  color: rgba(244,236,216,0.7);
  font-style: italic;
}}
.home-bar {{
  background: var(--ink-soft);
  padding: 0.5rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid var(--gold-dim);
}}
.home-bar a {{
  color: var(--gold);
  text-decoration: none;
  font-family: 'Cinzel', serif;
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}}
.home-bar a:hover {{ color: var(--parchment); }}
.main-wrap {{
  max-width: 900px;
  margin: 0 auto;
  padding: 1.5rem 1.5rem 4rem;
}}
section[id] {{
  background: var(--section-bg);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 1.5rem 1.75rem;
  margin-bottom: 1.5rem;
}}
section[id] h2 {{
  font-family: 'Cinzel', serif;
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--ink);
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
  letter-spacing: 0.03em;
}}
section[id] h2.outline-title {{
  font-size: 0.9rem;
  color: var(--gold-dim);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  border-bottom: none;
  margin-top: 0.5rem;
}}
section[id] h3 {{
  font-family: 'EB Garamond', serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--ink-soft);
  margin: 0.3rem 0;
  display: inline;
}}
ol.roman, ol.alpha, ol.decimal, ol.lower-alpha {{
  padding-left: 1.6rem;
  margin: 0.4rem 0;
}}
ol.roman {{ list-style-type: upper-roman; }}
ol.alpha {{ list-style-type: lower-alpha; }}
ol.decimal {{ list-style-type: decimal; }}
ol.lower-alpha {{ list-style-type: lower-alpha; }}
li {{ margin-bottom: 0.35rem; }}
li > ol {{ margin-top: 0.35rem; }}
.doctrine-tags {{
  margin-top: 1rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border);
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  align-items: center;
}}
.tag {{
  display: inline-block;
  background: var(--code-bg);
  border: 1px solid var(--border);
  color: var(--ink-soft);
  padding: 0.15em 0.55em;
  border-radius: 2px;
  font-size: 0.82rem;
}}
.verse-preview-tooltip {{
  background: var(--ink);
  color: var(--parchment);
  border: 1px solid var(--gold);
  border-radius: 4px;
  padding: 0.75rem 1rem;
  font-size: 0.88rem;
  line-height: 1.6;
  max-width: 420px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}
p.footnote {{
  font-size: 0.82rem;
  color: var(--gold-dim);
  border-top: 1px solid var(--border);
  padding-top: 0.5rem;
  margin-top: 0.5rem;
  font-style: italic;
}}
sup {{ font-size: 0.7em; color: var(--gold-dim); }}
a {{ color: var(--gold-dim); }}
a:hover {{ color: var(--ink); }}
.back-link {{
  display: inline-block;
  margin-top: 2rem;
  font-family: 'Cinzel', serif;
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--gold-dim);
  text-decoration: none;
  border-bottom: 1px solid var(--gold-dim);
}}
.back-link:hover {{ color: var(--ink); border-color: var(--ink); }}
@media (max-width: 640px) {{
  .site-header h1 {{ font-size: 1.4rem; }}
  .main-wrap {{ padding: 1rem 0.75rem 3rem; }}
  section[id] {{ padding: 1rem 1rem; }}
}}
</style>
</head>
<body>
<div class="home-bar">
  <a href="https://home.intelligencereport.info/">&#8592; Temple Door</a>
  <span style="color:var(--gold-dim);font-size:0.8rem;">|</span>
  <a href="doctrine-library.html">Doctrine Library</a>
</div>
<header class="site-header">
  <h1>{title}</h1>
  <p class="subtitle">Library of Christian Doctrines — IntelligenceReport.info</p>
</header>
<div class="main-wrap">
"""

FOOT_TEMPLATE = """
  <a class="back-link" href="doctrine-library.html">&#8592; Return to Doctrine Library</a>
</div>
</body>
</html>"""


def slug_to_title(slug):
    """Convert slug like 'divine-essence' to 'Doctrine of Divine Essence'."""
    return slug.replace("-", " ").title()


def main():
    print(f"Reading {SOURCE}...")
    html = SOURCE.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    sections = soup.find_all("section", id=True)
    print(f"Found {len(sections)} doctrine sections.")

    created = []
    for section in sections:
        slug = section["id"]
        # Get title from first h2 inside section
        h2 = section.find("h2")
        title = h2.get_text(strip=True) if h2 else slug_to_title(slug)

        out_path = OUT_DIR / f"{slug}.html"
        page = HEAD_TEMPLATE.format(title=title) + str(section) + FOOT_TEMPLATE

        out_path.write_text(page, encoding="utf-8")
        created.append((slug, title, out_path))
        print(f"  Created: {out_path.name}  ({title})")

    print(f"\nDone. {len(created)} doctrine pages created.")
    print("\nIndex entries (copy into doctrine-library.html index):")
    for slug, title, _ in created:
        print(f'  <li><a href="{slug}.html">{title}</a></li>')


if __name__ == "__main__":
    main()

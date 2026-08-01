"""
add_doctrine_buttons.py
Adds Phosphor icon action buttons to all individual doctrine pages.
Run from the doctrines folder
"""

from pathlib import Path

DOCTRINES_DIR = Path(".")

BUTTON_CSS = """
/* ── Action buttons ── */
.doc-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  padding: 0.6rem 1.5rem 0;
  background: var(--ink);
}
.doc-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.75rem;
  background: transparent;
  border: 1px solid rgba(184,151,58,0.4);
  border-radius: 3px;
  color: rgba(244,236,216,0.75);
  font-family: 'Cinzel', serif;
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  cursor: pointer;
  text-decoration: none;
  transition: border-color 0.15s, color 0.15s, background 0.15s;
  white-space: nowrap;
}
.doc-btn:hover {
  border-color: var(--gold);
  color: var(--gold);
  background: rgba(184,151,58,0.08);
}
.doc-btn svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}
@media (max-width: 640px) {
  .doc-actions { flex-wrap: wrap; gap: 0.35rem; padding: 0.5rem 0.75rem 0; }
  .doc-btn .btn-label { display: none; }
}
"""

BUTTON_HTML = """<div class="doc-actions">
  <!-- Export to PDF -->
  <button class="doc-btn" onclick="docAction('pdf')" title="Export to PDF">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor"><path d="M224,152a8,8,0,0,1-8,8H192v16h16a8,8,0,0,1,0,16H192v16a8,8,0,0,1-16,0V152a8,8,0,0,1,8-8h32A8,8,0,0,1,224,152ZM92,172a28,28,0,0,1-28,28H56v8a8,8,0,0,1-16,0V152a8,8,0,0,1,8-8H64A28,28,0,0,1,92,172Zm-16,0a12,12,0,0,0-12-12H56v24h8A12,12,0,0,0,76,172Zm88,8a36,36,0,0,1-36,36H112a8,8,0,0,1-8-8V152a8,8,0,0,1,8-8h16A36,36,0,0,1,164,180Zm-16,0a20,20,0,0,0-20-20h-8v40h8A20,20,0,0,0,148,180ZM40,116V40A16,16,0,0,1,56,24h96a8,8,0,0,1,5.66,2.34l56,56A8,8,0,0,1,216,88v28a8,8,0,0,1-16,0V96H152a8,8,0,0,1-8-8V40H56v76a8,8,0,0,1-16,0ZM160,80h28.69L160,51.31Z"/></svg>
    <span class="btn-label">PDF</span>
  </button>
  <!-- Share / Copy Link -->
  <button class="doc-btn" onclick="docAction('link')" title="Copy link">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor"><path d="M137.54,186.36a8,8,0,0,1,0,11.31l-9.94,10A56,56,0,0,1,48.38,128.4L72.5,104.28A56,56,0,0,1,149.31,102a8,8,0,1,1-10.64,12,40,40,0,0,0-54.85,1.63L59.7,139.72a40,40,0,1,0,56.58,56.58l9.94-9.94A8,8,0,0,1,137.54,186.36Zm70.08-138a56.08,56.08,0,0,0-79.22,0l-9.94,9.95a8,8,0,0,0,11.32,11.31l9.94-9.94a40,40,0,1,1,56.58,56.58L172.18,140.4A40,40,0,0,1,117.33,142a8,8,0,0,0-10.64,12,56,56,0,0,0,76.81-2.26l24.12-24.12A56.08,56.08,0,0,0,207.62,48.38Z"/></svg>
    <span class="btn-label">Link</span>
  </button>
  <!-- Copy to Clipboard -->
  <button class="doc-btn" onclick="docAction('clipboard')" title="Copy text to clipboard">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor"><path d="M165.66,2.34a8,8,0,0,0-11.32,0L136,20.69l-6.34-6.35a8,8,0,0,0-11.32,11.32L128,35.31l-96,96V224a8,8,0,0,0,8,8H232a8,8,0,0,0,8-8V131.31Zm-128,201,75.51-75.51,18.34,18.34L56,221.37ZM224,216H179.31l-30.62-30.63,18.34-18.34L224,224Zm0-42.63-82.34-82.34,16-16L224,151.37ZM152,69,51.31,169.66,40,158.34,140.69,57.66ZM165.66,56,144,77.66,139.31,73l21.66-21.65Z"/></svg>
    <span class="btn-label">Copy</span>
  </button>
  <!-- Download as Image -->
  <button class="doc-btn" onclick="docAction('image')" title="Download as image">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor"><path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,16V158.75l-26.07-26.06a16,16,0,0,0-22.63,0l-20,20-44-44a16,16,0,0,0-22.62,0L40,149.37V56ZM40,200V172l52-52,44,44,28-28,52,52.07V200Zm84-104a12,12,0,1,1,12,12A12,12,0,0,1,124,96Z"/></svg>
    <span class="btn-label">Image</span>
  </button>
  <!-- Copy as HTML -->
  <button class="doc-btn" onclick="docAction('html')" title="Copy as HTML">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor"><path d="M216,88H152V40a8,8,0,0,0-8-8H56A16,16,0,0,0,40,48V208a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V96A8,8,0,0,0,216,88Zm-56,0V51.31L208.69,88ZM56,208V48h80V96a8,8,0,0,0,8,8h56V208Zm130.34-82.34a8,8,0,0,1,0,11.31L165.66,158l20.68,20.69a8,8,0,0,1-11.32,11.31l-26.34-26.34a8,8,0,0,1,0-11.32l26.34-26.34A8,8,0,0,1,186.34,125.66Zm-96,11.31L110.34,158,89.66,178.69A8,8,0,0,1,78.34,167.38L99,146.66,78.34,126a8,8,0,1,1,11.32-11.31Z"/></svg>
    <span class="btn-label">HTML</span>
  </button>
  <!-- Embed Code -->
  <button class="doc-btn" onclick="docAction('embed')" title="Get embed code">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" fill="currentColor"><path d="M69.12,94.15,28.5,128l40.62,33.85a8,8,0,1,1-10.24,12.29l-48-40a8,8,0,0,1,0-12.29l48-40a8,8,0,0,1,10.24,12.3Zm176,27.7-48-40a8,8,0,1,0-10.24,12.3L227.5,128l-40.62,33.85a8,8,0,1,0,10.24,12.29l48-40a8,8,0,0,0,0-12.29ZM162.73,32.48a8,8,0,0,0-10.25,4.79l-64,176a8,8,0,0,0,4.79,10.26A8.14,8.14,0,0,0,96,224a8,8,0,0,0,7.52-5.27l64-176A8,8,0,0,0,162.73,32.48Z"/></svg>
    <span class="btn-label">Embed</span>
  </button>
</div>
<script>
(function() {
  function docAction(type) {
    const section = document.querySelector('section[id]');
    const title = document.querySelector('.site-header h1') ?
      document.querySelector('.site-header h1').textContent : document.title;
    if (type === 'link') {
      navigator.clipboard.writeText(window.location.href)
        .then(() => flash('Link copied!'));
    } else if (type === 'clipboard') {
      const text = section ? section.innerText : document.body.innerText;
      navigator.clipboard.writeText(text)
        .then(() => flash('Text copied!'));
    } else if (type === 'html') {
      const html = section ? section.outerHTML : '';
      navigator.clipboard.writeText(html)
        .then(() => flash('HTML copied!'));
    } else if (type === 'embed') {
      const embed = '<iframe src="' + window.location.href +
        '" width="100%" height="600" frameborder="0"></iframe>';
      navigator.clipboard.writeText(embed)
        .then(() => flash('Embed code copied!'));
    } else if (type === 'pdf') {
      window.print();
    } else if (type === 'image') {
      flash('Select Print > Save as PDF, then use an image converter.');
    }
  }
  window.docAction = docAction;
  function flash(msg) {
    const el = document.createElement('div');
    el.textContent = msg;
    el.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;background:#2a2118;color:#f4ecd8;' +
      'padding:0.6rem 1.2rem;border-radius:4px;font-family:Cinzel,serif;font-size:0.75rem;' +
      'letter-spacing:0.1em;z-index:9999;border:1px solid #b8973a;';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2200);
  }
})();
</script>"""

SKIP_FILES = {
    "doctrine-library.html",
    "scripture-index.html",
    "index.html",
    "20260801_001_split_doctrines.py",
    "20260801_002_doctrine-library.html",
    "split_doctrines.py",
}

def process_file(path: Path):
    content = path.read_text(encoding="utf-8")

    # Skip if already has buttons
    if "doc-actions" in content:
        print(f"  SKIP (already has buttons): {path.name}")
        return

    # Add CSS before </style>
    if "</style>" in content:
        content = content.replace("</style>", BUTTON_CSS + "\n</style>", 1)
    else:
        print(f"  WARN: no </style> found in {path.name}")
        return

    # Add button HTML after <header class="site-header"> closing tag
    if '</header>' in content:
        content = content.replace('</header>', '</header>\n' + BUTTON_HTML, 1)
    else:
        print(f"  WARN: no </header> found in {path.name}")
        return

    path.write_text(content, encoding="utf-8")
    print(f"  OK: {path.name}")


def main():
    html_files = [
        f for f in DOCTRINES_DIR.glob("*.html")
        if f.name not in SKIP_FILES
    ]
    print(f"Processing {len(html_files)} doctrine pages...")
    for f in sorted(html_files):
        process_file(f)
    print("Done.")


if __name__ == "__main__":
    main()

"""
fix_image_download.py
Replaces the placeholder image action with html2canvas download.
Run from the doctrines folder.
"""

from pathlib import Path

SKIP_FILES = {
    "doctrine-library.html",
    "scripture-index.html",
    "index.html",
    "20260801_001_split_doctrines.py",
    "20260801_002_doctrine-library.html",
    "split_doctrines.py",
    "add_doctrine_buttons.py",
    "fix_image_download.py",
}

OLD_SCRIPT = "} else if (type === 'image') {\n      flash('Select Print > Save as PDF, then use an image converter.');\n    }"

NEW_SCRIPT = """} else if (type === 'image') {
      const section = document.querySelector('section[id]');
      if (!section) { flash('Nothing to capture.'); return; }
      flash('Preparing image\u2026');
      import('https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.esm.min.js')
        .then(mod => {
          const h2c = mod.default || mod;
          return h2c(section, { backgroundColor: '#fdfbf5', scale: 2, useCORS: true });
        })
        .then(canvas => {
          const link = document.createElement('a');
          link.download = (document.querySelector('.site-header h1') ?
            document.querySelector('.site-header h1').textContent.trim().replace(/\\s+/g, '-').toLowerCase()
            : 'doctrine') + '.png';
          link.href = canvas.toDataURL('image/png');
          link.click();
          flash('Image downloaded!');
        })
        .catch(() => flash('Image export failed. Try PDF instead.'));
    }"""

def main():
    files = [f for f in Path(".").glob("*.html") if f.name not in SKIP_FILES]
    print(f"Processing {len(files)} files...")
    fixed = 0
    for f in sorted(files):
        content = f.read_text(encoding="utf-8")
        if OLD_SCRIPT in content:
            content = content.replace(OLD_SCRIPT, NEW_SCRIPT)
            f.write_text(content, encoding="utf-8")
            print(f"  OK: {f.name}")
            fixed += 1
        else:
            print(f"  SKIP: {f.name}")
    print(f"Done. {fixed} files updated.")

if __name__ == "__main__":
    main()

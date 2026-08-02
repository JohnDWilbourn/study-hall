"""
build_content_index.py
Scans lessons, illuminations, and watchman content,
assigns tags from the doctrine taxonomy, and writes content-index.json.
Run from: /home/johndavid/Projects/Websites/
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# ── Tag taxonomy with keyword signals ────────────────────────────────────────
TAG_KEYWORDS = {
    "Angels":           ["angel", "angelic", "cherub", "seraph", "elect angel", "fallen angel", "demon"],
    "Angelology":       ["angelology", "angelic conflict", "angel of yahweh", "angel of the lord"],
    "Christ":           ["christ", "jesus", "messiah", "incarnat", "hypostatic", "kenosis", "lord jesus"],
    "Church Age":       ["church age", "royal family", "body of christ", "pentecost", "rapture", "mystery doctrine"],
    "Divine Attributes":["omniscien", "omnipoten", "omnipresent", "immutab", "sovereignty", "righteousness of god", "justice of god", "veracity", "love of god", "eternal life of god"],
    "Divine Discipline":["divine discipline", "sin unto death", "cursing", "warning discipline", "intensive discipline"],
    "Doctrine":         ["doctrine", "bible doctrine", "word of god", "scripture", "exegesis"],
    "Faith":            ["faith", "belief", "trust", "faith-rest", "non-meritorious"],
    "Giving":           ["giving", "tithe", "offering", "tenth", "financial"],
    "Grace":            ["grace", "logistical grace", "grace policy", "grace orientation", "grace provision", "supergrace", "ultra-supergrace"],
    "Happiness":        ["happiness", "joy", "contentment", "sharing the happiness of god"],
    "History":          ["history", "human history", "angelic history", "historical", "dispensation"],
    "Holy Spirit":      ["holy spirit", "filling of the spirit", "spirit-filled", "grieving the spirit", "quenching the spirit", "indwelling", "baptism of the spirit", "pneumatology"],
    "Mental Attitude":  ["mental attitude", "heart", "right lobe", "left lobe", "scar tissue", "blackout", "conscience", "volition", "thinking"],
    "Position in Christ":["position in christ", "union with christ", "in christ", "positional truth", "current positional", "retroactive positional"],
    "Prayer":           ["prayer", "intercession", "petition", "praying"],
    "Priesthood":       ["priest", "priesthood", "levitical", "royal priest", "high priest"],
    "Prophecy":         ["prophecy", "prophetic", "eschatology", "millennium", "tribulation", "second advent", "rapture"],
    "Salvation":        ["salvation", "save", "saved", "born again", "regenerat", "eternal life", "justif", "redempt", "reconcil", "propitiat", "adjustment to the justice"],
    "Satan":            ["satan", "devil", "lucifer", "cosmic system", "demonism", "satanic"],
    "Sin":              ["sin", "old sin nature", "sin nature", "hamartiology", "carnality", "reversionism", "rebound"],
    "Sovereignty":      ["sovereignty", "sovereign", "divine decree", "will of god", "omniscien"],
    "Spiritual Growth":  ["spiritual growth", "maturity", "supergrace", "ultra-supergrace", "advance", "spiritual adult", "spiritual maturity"],
    "Spiritual Life":   ["spiritual life", "christian way of life", "protocol plan", "plan of god", "execution of the plan"],
    "Spiritual Warfare":["spiritual warfare", "angelic conflict", "invisible war", "cosmic system", "satan's strategy"],
    "Theology Proper":  ["theology proper", "divine essence", "godhead", "trinity", "god the father", "attributes of god"],
    "Typology":         ["typology", "type", "shadow", "foreshadow", "mosaic law", "levitical"],
}

def extract_text(html_path):
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    for tag in soup(["script", "style", "nav"]):
        tag.decompose()
    return soup.get_text(" ", strip=True).lower()

def extract_title(html_path):
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    title = soup.find("title")
    if title:
        return title.get_text(strip=True).split("—")[0].strip()
    return html_path.stem

def assign_tags(text):
    tags = []
    for tag, keywords in TAG_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                tags.append(tag)
                break
    return sorted(set(tags))

def scan_lessons(base):
    results = []
    lessons_dir = base / "Spiritual_Growth_Lessons/spiritual-growth-lessons/lessons"
    if not lessons_dir.exists():
        print(f"  WARNING: lessons dir not found at {lessons_dir}")
        return results
    for f in sorted(lessons_dir.glob("*.html")):
        text = extract_text(f)
        title = extract_title(f)
        tags = assign_tags(text)
        slug = f.name
        url = f"https://lessons.intelligencereport.info/lessons/{slug}"
        results.append({"title": title, "url": url, "file": slug, "tags": tags})
        print(f"  lesson: {slug} → {len(tags)} tags")
    return results

def scan_illuminations(base):
    results = []
    illum_dir = base / "Romans_Website/romans-commentary/illuminations"
    if not illum_dir.exists():
        illum_dir = base / "Romans_Website/romans-commentary-git/illuminations"
    if not illum_dir.exists():
        print(f"  WARNING: illuminations dir not found")
        return results
    skip = {"illuminations.html", "index.html"}
    for f in sorted(illum_dir.glob("*.html")):
        if f.name in skip:
            continue
        text = extract_text(f)
        title = extract_title(f)
        tags = assign_tags(text)
        url = f"https://commentary.intelligencereport.info/illuminations/{f.name}"
        results.append({"title": title, "url": url, "file": f.name, "tags": tags})
        print(f"  illumination: {f.name} → {len(tags)} tags")
    return results

def scan_watchman(base):
    results = []
    watchman_dir = base / "the-watchman"
    if not watchman_dir.exists():
        print(f"  WARNING: watchman dir not found")
        return results
    skip = {"index.html"}
    for f in sorted(watchman_dir.glob("*.html")):
        if f.name in skip:
            continue
        text = extract_text(f)
        title = extract_title(f)
        tags = assign_tags(text)
        url = f"https://watchman.intelligencereport.info/{f.name}"
        results.append({"title": title, "url": url, "file": f.name, "tags": tags})
        print(f"  watchman: {f.name} → {len(tags)} tags")
    return results

def main():
    base = Path("/home/johndavid/Projects/Websites")

    print("Scanning lessons...")
    lessons = scan_lessons(base)

    print("Scanning illuminations...")
    illuminations = scan_illuminations(base)

    print("Scanning watchman...")
    watchman = scan_watchman(base)

    index = {
        "lessons": lessons,
        "illuminations": illuminations,
        "watchman": watchman,
    }

    out = base / "study-hall/content-index.json"
    out.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten: {out}")
    print(f"  {len(lessons)} lessons, {len(illuminations)} illuminations, {len(watchman)} watchman articles")

if __name__ == "__main__":
    main()

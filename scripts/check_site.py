from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
HTML = sorted(ROOT.glob("*.html"))
assert HTML, "No HTML files found"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(v for k, v in attrs if k == "href" and v)

for page in HTML:
    parser = Links()
    parser.feed(page.read_text(encoding="utf-8"))
    for href in parser.hrefs:
        if href.startswith(("http://","https://","mailto:","tel:","#")):
            continue
        target = href.split("#",1)[0].split("?",1)[0]
        if target:
            assert (ROOT / target).exists(), f"{page.name}: broken local link {href}"

required = ["index.html","people-operations.html","technology.html","about.html","styles.css","script.js","favicon.svg"]
for name in required:
    assert (ROOT / name).exists(), f"Missing {name}"

print(f"Verified {len(HTML)} HTML pages and local links.")

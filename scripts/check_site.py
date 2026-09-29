from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
HTML = sorted(ROOT.glob("*.html"))
assert HTML, "No HTML files found"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.title = ""
        self.in_title = False
        self.has_description = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])
        if tag == "meta" and attrs.get("name") == "description" and attrs.get("content"):
            self.has_description = True
        if tag == "title":
            self.in_title = True
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title += data

for page in HTML:
    text = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    assert parser.title.strip(), f"{page.name}: missing title"
    if page.name != "404.html":
        assert parser.has_description, f"{page.name}: missing meta description"
    for href in parser.hrefs:
        if href.startswith(("http://","https://","mailto:","tel:","#")):
            continue
        target = href.split("#",1)[0].split("?",1)[0]
        if target:
            assert (ROOT / target).exists(), f"{page.name}: broken local link {href}"

public_text = "\n".join(p.read_text(encoding="utf-8").lower() for p in HTML)
for excluded in ("loan", "lending", "financial assistance"):
    assert excluded not in public_text, f"Public HTML unexpectedly mentions: {excluded}"

required = ["index.html","people-operations.html","technology.html","about.html","contact.html","privacy.html","terms.html","styles.css","script.js","favicon.svg","logo-mark.svg","robots.txt","sitemap.xml"]
for name in required:
    assert (ROOT / name).exists(), f"Missing {name}"

for expected in ("adegheprofessionalservices@gmail.com", "+234 703 035 1005", "+234 905 672 6687"):
    assert expected in (ROOT / "contact.html").read_text(encoding="utf-8"), f"Missing contact detail: {expected}"
about_text = (ROOT / "about.html").read_text(encoding="utf-8")
for expected in ("Joy Adesuwa Omokaro", "Founder & Principal", "Aighewi Eghosa", "Technology Lead"):
    assert expected in about_text, f"Missing leadership detail: {expected}"
assert "https://adegheprofessionalservices.com/" in (ROOT / "sitemap.xml").read_text(encoding="utf-8")
print(f"Verified {len(HTML)} HTML pages, metadata, scope, contacts and local links.")

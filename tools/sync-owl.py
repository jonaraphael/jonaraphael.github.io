"""Publish OWL's two HTML pages while serving assets from the project deployment."""

from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from xml.etree.ElementTree import Element

import html5lib

SOURCE = "https://jonaraphael.com/offline-wandering-library/"
MOUNT = "/owl/"
PAGES = {"index.html": MOUNT, "builder.html": MOUNT + "builder.html"}
NAVIGATION = {urljoin(SOURCE, name): path for name, path in PAGES.items()}
NAVIGATION[SOURCE] = MOUNT


def mounted_page(filename):
    url = urljoin(SOURCE, filename)
    request = Request(url, headers={"Cache-Control": "no-cache"})
    with urlopen(request, timeout=45) as response:
        if response.geturl() != url or response.headers.get_content_type() != "text/html":
            raise ValueError(f"Unexpected page at {url}")
        page = html5lib.parse(response.read().decode("utf-8"), namespaceHTMLElements=False)

    head = page.find("head")
    if "Offline Wandering Library" not in head.findtext("title", "") or head.find("base") is not None:
        raise ValueError(f"Unexpected OWL document at {url}")

    # The builder fetches its catalogs and mirror pieces relative to the document.
    # Permit only its published asset directory as the base. Keep the remaining CSP.
    if filename == "builder.html":
        policy = next(meta for meta in head.findall("meta")
                      if meta.get("http-equiv", "").lower() == "content-security-policy")
        directives = [part.strip() for part in policy.get("content").split(";")]
        directives[directives.index("base-uri 'none'")] = "base-uri " + SOURCE
        policy.set("content", "; ".join(directives))
        head.insert(list(head).index(policy) + 1, Element("base", {"href": SOURCE}))

    # Keep navigation on the short URL and leave SVG fragment references local.
    for anchor in page.iter("a"):
        href = anchor.get("href")
        if href is None:
            continue
        if href.startswith("#"):
            if filename == "builder.html":
                anchor.set("href", PAGES[filename] + href)
            continue
        target = urlsplit(urljoin(url, href))
        path = NAVIGATION.get(target._replace(query="", fragment="").geturl())
        anchor.set("href", urlunsplit(("", "", path, target.query, target.fragment)) if path else target.geturl())

    for tag, attr in (("script", "src"), ("link", "href"), ("img", "src"), ("source", "src")):
        for node in page.iter(tag):
            if node.get(attr):
                node.set(attr, urljoin(url, node.get(attr)))

    html = html5lib.serialize(page, omit_optional_tags=False, quote_attr_values="always")
    return "<!doctype html>\n" + html + "\n"


if __name__ == "__main__":
    pages = {name: mounted_page(name) for name in PAGES}
    output = Path(__file__).resolve().parents[1] / "owl"
    output.mkdir(exist_ok=True)
    for name, html in pages.items():
        (output / name).write_text(html, encoding="utf-8")

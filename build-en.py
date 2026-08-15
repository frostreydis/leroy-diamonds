#!/usr/bin/env python3
"""
build-en.py

Generates en/index.html — a real, separately-crawlable English version of
the homepage — from index.html (the Slovak default).

Why a separate file instead of relying on the in-page language switch?
Search engines index a URL's own default content. A JS toggle that swaps
text on the same URL works fine for visitors, but Google still primarily
sees/indexes the Slovak version at "/". Having a genuine /en/index.html
lets us point proper hreflang tags at two distinct URLs, so Google can
serve the right language to the right searcher.

What this script does:
  1. Parses index.html.
  2. For every element carrying a data-en="..." attribute, replaces its
     visible content with that English text (same mechanism the in-page
     JS switch already uses — this script just "bakes in" the English
     version at build time instead of at runtime).
  3. Swaps English-language <title>, meta description, Open Graph /
     Twitter / JSON-LD strings.
  4. Sets <html lang="en">, flips the active state of the SK/EN switch,
     and points canonical + hreflang + og:url at the /en/ URL.
  5. Rewrites the handful of same-site relative paths (favicon links,
     the SK/EN switch hrefs, the remembered-language redirect script,
     and the image-manifest fetch paths in the JS) with a "../" prefix,
     since en/index.html lives one folder deeper than index.html.

Run this again any time you edit content in index.html — it always
regenerates en/index.html from scratch, so don't hand-edit that file.

Note: every same-site link/asset path in index.html is written
*relative* (e.g. "images/...", "favicon.svg", href="en/") rather than
root-absolute ("/images/...") — that's what lets this same pair of files
work correctly whether the site ends up served from a domain root, a
custom domain, or a GitHub Pages *project* subpath like
"username.github.io/repo-name/". Only hreflang/canonical/Open Graph URLs
(which the spec requires to be absolute) hardcode the real domain — see
README for what to update there if the final domain differs.

Usage:
    python3 build-en.py
"""

import re
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit(
        "This script needs BeautifulSoup4. Install it with:\n"
        "    pip install beautifulsoup4\n"
    )

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "index.html"
DEST_DIR = ROOT / "en"
DEST = DEST_DIR / "index.html"

TITLE_EN = "Leroy Diamonds — Fine Jewelry Bratislava | Custom Jewelry"
DESCRIPTION_EN = (
    "Leroy Diamonds — a jewelry atelier in Bratislava. Handcrafted diamond "
    "jewelry, engagement rings and bespoke pieces. Certified diamonds, "
    "made to order."
)
JSONLD_DESCRIPTION_EN = (
    "A jewelry atelier in Bratislava. Handcrafted diamond jewelry, "
    "engagement rings and bespoke pieces."
)

# Relative asset href/src values in index.html that need a "../" prefix
# once the file is copied one folder deeper, into en/.
RELATIVE_ASSET_PREFIXES = ("favicon", "apple-touch-icon.png")


def main():
    html = SRC.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # 1) <html lang="en">
    soup.html["lang"] = "en"

    # 2) Bake in English text for every data-en element (mirrors the
    #    runtime JS so the page is correct even before JS runs).
    for el in soup.select("[data-en]"):
        # data-en may contain simple inline HTML (e.g. <em>); parse it
        # as a mini fragment so tags like <em> survive.
        fragment = BeautifulSoup(el["data-en"], "html.parser")
        el.clear()
        el.append(fragment)

    for el in soup.select("[data-en-ph]"):
        el["placeholder"] = el["data-en-ph"]

    # 3) Title / meta description / OG / Twitter / JSON-LD
    if soup.title:
        soup.title.string = TITLE_EN

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        meta_desc["content"] = DESCRIPTION_EN

    for prop, value in [
        ("og:title", TITLE_EN),
        ("og:description", DESCRIPTION_EN),
        ("og:url", "https://leroydiamonds.sk/en/"),
        ("og:locale", "en_US"),
    ]:
        tag = soup.find("meta", attrs={"property": prop})
        if tag:
            tag["content"] = value
    og_locale_alt = soup.find("meta", attrs={"property": "og:locale:alternate"})
    if og_locale_alt:
        og_locale_alt["content"] = "sk_SK"

    for name, value in [
        ("twitter:title", "Leroy Diamonds — Fine Jewelry Bratislava"),
        ("twitter:description", DESCRIPTION_EN),
    ]:
        tag = soup.find("meta", attrs={"name": name})
        if tag:
            tag["content"] = value

    canonical = soup.find("link", attrs={"rel": "canonical"})
    if canonical:
        canonical["href"] = "https://leroydiamonds.sk/en/"

    lang_meta = soup.find("meta", attrs={"name": "language"})
    if lang_meta:
        lang_meta["content"] = "English"

    jsonld = soup.find("script", attrs={"type": "application/ld+json"})
    if jsonld and jsonld.string:
        jsonld.string = jsonld.string.replace(
            "Klenotnícky ateliér v Bratislave. Ručne vyrábané diamantové "
            "šperky, zásnubné prstene a šperky na mieru.",
            JSONLD_DESCRIPTION_EN,
        ).replace(
            '"url": "https://leroydiamonds.sk/"',
            '"url": "https://leroydiamonds.sk/en/"',
        )

    # 4) Flip the active SK/EN switch state + fix the switch's own hrefs.
    #    On index.html these are written from the root's point of view
    #    (SK="./" self, EN="en/" down); from en/'s point of view it's the
    #    mirror image (EN="./" self, SK="../" up).
    for a in soup.select(".lang-btn"):
        lang = a.get("data-lang-btn")
        if lang == "en":
            a["class"] = a.get("class", []) + ["active"]
            a["aria-current"] = "page"
            a["href"] = "./"
        else:
            classes = [c for c in a.get("class", []) if c != "active"]
            a["class"] = classes
            if a.has_attr("aria-current"):
                del a["aria-current"]
            a["href"] = "../"

    # 5) Prefix same-site relative asset paths with "../" for the new
    #    file depth (favicon / apple-touch-icon <link> tags).
    for link in soup.find_all("link"):
        href = link.get("href")
        if href and href.startswith(RELATIVE_ASSET_PREFIXES):
            link["href"] = "../" + href

    # 6) The remembered-language redirect script: on index.html this
    #    only needs to handle "saved == en" (go down into en/); the en/
    #    copy needs the mirror check ("saved == sk" (go back up).
    redirect_script = soup.find("script", id="lang-redirect")
    if redirect_script:
        redirect_script.string = (
            "\n  (function(){\n"
            "    try{\n"
            "      var saved = localStorage.getItem('leroydiamonds_lang');\n"
            "      if(saved === 'sk'){ location.replace('../'); }\n"
            "    }catch(e){ /* storage unavailable — stay on default */ }\n"
            "  })();\n"
        )

    # 7) Image-manifest fetch paths in the main <script>: prefix the two
    #    "images/..." template-literal occurrences with "../".
    main_script = None
    for s in soup.find_all("script"):
        if s.string and "fetchManifest" in s.string:
            main_script = s
            break
    if main_script:
        main_script.string = main_script.string.replace(
            "fetch(`images/", "fetch(`../images/"
        ).replace(
            "src: `images/", "src: `../images/"
        )

    DEST_DIR.mkdir(exist_ok=True)
    # BeautifulSoup's html.parser output is close to source but not
    # byte-identical; that's fine for a generated file.
    DEST.write_text(str(soup), encoding="utf-8")
    print(f"Generated {DEST.relative_to(ROOT)} ({DEST.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

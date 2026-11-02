#!/usr/bin/env python3
"""Builds every HTML page of HisaabPK from the content in scripts/pages.py.

Run from the repo root:  python3 scripts/build.py
Change BASE_URL in scripts/pages.py once a custom domain is bought, then rebuild.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pages as P  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = P.ASSET_VERSION

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="5" y="3" width="22" height="26" rx="2" fill="var(--green)"/>'
        '<path d="M5 26l3 3 3-3 3 3 3-3 3 3 3-3 3 3 2-2v3H5z" fill="var(--paper)"/>'
        '<rect x="9" y="9" width="14" height="2" rx="1" fill="#fff" opacity=".75"/>'
        '<rect x="9" y="14" width="10" height="2" rx="1" fill="#fff" opacity=".75"/>'
        '<rect x="9" y="19" width="14" height="3" rx="1" fill="var(--marigold)"/></svg>')

THEME_INIT = ("<script>try{var t=localStorage.getItem('hpk-theme');"
              "if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>")


def url(slug):
    return P.BASE_URL + ("/" + slug + "/" if slug else "/")


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def head(pg, ld):
    t = html.escape(pg["title"])
    d = html.escape(pg["description"])
    u = url(pg["slug"])
    robots = "noindex" if pg.get("noindex") else "index, follow"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{u}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#f7f9f6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101814" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{P.SITE_NAME}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{u}">
<meta property="og:locale" content="en_PK">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/assets/style.css?v={V}">
{THEME_INIT}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def nav(active):
    links = [("", "All calculators"), ("about", "About"), ("contact", "Contact")]
    items = "".join(
        f'<a href="{"/" + s + "/" if s else "/"}"{" aria-current=\"page\"" if s == active else ""}>{n}</a>'
        for s, n in links)
    return f"""<header class="site-nav"><div class="wrap">
<a class="logo" href="/" aria-label="{P.SITE_NAME} home">{LOGO}<span>Hisaab<span class="pk">PK</span></span></a>
<nav class="nav-links" aria-label="Main">{items}</nav>
</div></header>
"""


def foot(scripts):
    tags = "".join(f'<script src="/assets/{s}?v={V}" defer></script>' for s in ["common.js"] + scripts)
    tools = "".join(f'<a href="/{t["slug"]}/">{t["short"]}</a>' for t in P.TOOLS)
    return f"""<footer class="site-foot"><div class="wrap">
<nav aria-label="Calculators">{tools}</nav>
<nav aria-label="Site"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy-policy/">Privacy policy</a><a href="/terms/">Terms and disclaimer</a></nav>
<p style="margin:0;flex-basis:100%;display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap"><span>© 2026 {P.SITE_NAME}. Free calculators for Pakistan. Figures are estimates; check official sources for decisions.</span><button type="button" class="theme-toggle" id="theme-toggle">Dark mode</button></p>
</div></footer>
{tags}
</body>
</html>
"""


def crumbs(pg):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / '
            f'<span aria-current="page">{html.escape(pg["short"])}</span></nav>')


def faq_html(faq):
    out = ['<h2 id="faq">Questions people ask</h2>']
    for q, a in faq:
        out.append(f"<details><summary>{q}</summary><div>{a}</div></details>")
    return "\n".join(out)


def related(pg):
    links = [t for t in P.TOOLS if t["slug"] != pg["slug"]][:4]
    items = "".join(f'<li><a href="/{t["slug"]}/">{t["short"]}</a>: {t["question"]}</li>' for t in links)
    return f'<section class="related article"><h2 style="margin-top:0">More calculators</h2><ul>{items}</ul></section>'


def tool_ld(pg):
    u = url(pg["slug"])
    graph = [
        {"@type": "WebApplication", "name": pg["h1"], "url": u, "description": pg["description"],
         "applicationCategory": pg.get("category", "FinanceApplication"), "operatingSystem": "Any",
         "inLanguage": "en-PK", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "PKR"},
         "dateModified": P.CHECKED_ISO},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": url("")},
            {"@type": "ListItem", "position": 2, "name": pg["short"], "item": u}]},
    ]
    if pg.get("faq"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q),
             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in pg["faq"]]})
    return {"@context": "https://schema.org", "@graph": graph}


def tool_page(pg):
    body = f"""{nav(None)}<main id="main" class="page"><div class="wrap">
{crumbs(pg)}
<header class="tool-head">
<h1>{pg["h1"]}</h1>
<p class="lede">{pg["lede"]}</p>
<p class="checked">{pg.get("checked_label", "Rates checked")} {P.CHECKED}</p>
</header>
<div class="calc">
<form id="calc-form" class="panel" novalidate autocomplete="off">
{pg["form"]}
</form>
<aside class="slip" id="result" aria-live="polite"><p class="slip-title">Result</p><p class="empty">Loading the calculator…</p></aside>
</div>
<div class="article">
{pg["article"]}
{faq_html(pg["faq"])}
<h2>Sources</h2>
<p class="sources">{pg["sources"]}</p>
</div>
{related(pg)}
</div></main>
"""
    return head(pg, tool_ld(pg)) + body + foot(pg["scripts"])


def info_page(pg):
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": pg["title"], "url": url(pg["slug"])}
    body = f"""{nav(pg["slug"])}<main id="main" class="page"><div class="wrap">
<div class="article">
<h1 style="margin-top:2rem">{pg["h1"]}</h1>
{pg["body"]}
</div>
</div></main>
"""
    return head(pg, ld) + body + foot([])


def home_page():
    pg = P.HOME
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": P.SITE_NAME, "url": url(""), "description": pg["description"], "inLanguage": "en-PK"},
        {"@type": "Organization", "name": P.SITE_NAME, "url": url(""), "logo": P.BASE_URL + "/favicon.svg",
         "email": P.EMAIL}]}
    rows = "".join(
        f'<li><a href="/{t["slug"]}/"><span class="name">{t["short"]}</span>'
        f'<span class="q">{t["question"]}</span><span class="when">{t["when"]}</span></a></li>'
        for t in P.TOOLS)
    body = f"""{nav("")}<main id="main"><div class="wrap">
<section class="home-hero">
<div>
<h1>{pg["h1"]}</h1>
<p class="lede">{pg["lede"]}</p>
<p><a href="#tools">See all {len(P.TOOLS)} calculators</a></p>
</div>
<div class="quick-calc">
<form id="calc-form" class="panel" novalidate autocomplete="off" style="margin-bottom:1rem">
<div class="field"><label for="salary">What is your monthly salary?</label>
<div class="money"><span>Rs</span><input id="salary" type="text" inputmode="numeric" placeholder="150,000" value="150000"></div>
<input type="radio" name="period" value="month" checked hidden></div>
<p class="hint" style="margin:0">Tax for 2026-27. <a href="/salary-tax-calculator/">Open the full tax calculator</a></p>
</form>
<aside class="slip" id="result" aria-live="polite" data-compact></aside>
</div>
</section>
<h2 id="tools" style="margin-top:1rem">Calculators</h2>
<ul class="index">{rows}</ul>
<div class="article">{pg["body"]}</div>
</div></main>
"""
    return head(pg, ld) + body + foot(["tools/salary-tax.js"])


def not_found():
    pg = {"slug": "404", "title": "Page not found | " + P.SITE_NAME, "description": "This page does not exist.", "noindex": True}
    rows = "".join(f'<li><a href="/{t["slug"]}/">{t["short"]}</a></li>' for t in P.TOOLS)
    body = f"""{nav(None)}<main id="main" class="page"><div class="wrap"><div class="article">
<h1 style="margin-top:2rem">This page doesn't exist</h1>
<p>The link may be old or mistyped. Pick a calculator instead:</p><ul>{rows}</ul>
</div></div></main>
"""
    return head(pg, {"@context": "https://schema.org", "@type": "WebPage", "name": "Not found"}) + body + foot([])


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    write("index.html", home_page())
    for pg in P.TOOLS:
        write(f'{pg["slug"]}/index.html', tool_page(pg))
    for pg in P.INFO:
        write(f'{pg["slug"]}/index.html', info_page(pg))
    write("404.html", not_found())

    urls = [("", "1.0")] + [(t["slug"], "0.9") for t in P.TOOLS] + [(p["slug"], "0.3") for p in P.INFO]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for s, pr in urls:
        sm.append(f"  <url><loc>{url(s)}</loc><lastmod>{P.CHECKED_ISO}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {P.BASE_URL}/sitemap.xml\n")
    print(f"Built {1 + len(P.TOOLS) + len(P.INFO) + 1} pages for {P.BASE_URL}")


if __name__ == "__main__":
    main()

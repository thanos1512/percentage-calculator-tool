#!/usr/bin/env python3
"""Builds every HTML page of PakCalculators from the content in scripts/pages.py.

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

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="3" y="2" width="26" height="28" rx="7" fill="#0e7a55"/>'
        '<rect x="7.5" y="6.5" width="17" height="6.5" rx="2" fill="#fff"/>'
        '<circle cx="10.5" cy="18.5" r="2" fill="#fff" opacity=".85"/><circle cx="16" cy="18.5" r="2" fill="#fff" opacity=".85"/>'
        '<circle cx="21.5" cy="18.5" r="2" fill="#f5b82e"/><circle cx="10.5" cy="24" r="2" fill="#fff" opacity=".85"/>'
        '<circle cx="16" cy="24" r="2" fill="#fff" opacity=".85"/><circle cx="21.5" cy="24" r="2" fill="#fff" opacity=".85"/></svg>')

def svg(paths, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{paths}</svg>'


ICONS = {
    "tax": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9.5 14.5l5-5"/><circle cx="9.5" cy="9.5" r=".9"/><circle cx="14.5" cy="14.5" r=".9"/>',
    "age-job": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><circle cx="9" cy="11" r="2.2"/><path d="M5.8 16.5c.6-1.5 1.8-2.3 3.2-2.3s2.6.8 3.2 2.3"/><path d="M14.5 10h4M14.5 13.5h3"/>',
    "power": '<path d="M13 2.5L4.5 13.5H11l-1 8 8.5-11H12z"/>',
    "zakat": '<ellipse cx="12" cy="6" rx="7" ry="2.8"/><path d="M5 6v6c0 1.6 3.1 2.8 7 2.8s7-1.2 7-2.8V6"/><path d="M5 12v6c0 1.6 3.1 2.8 7 2.8s7-1.2 7-2.8v-6"/>',
    "marks": '<path d="M18.5 5.5l-13 13"/><circle cx="7" cy="7" r="2.6"/><circle cx="17" cy="17" r="2.6"/>',
    "gpa": '<path d="M2.5 9L12 4.5 21.5 9 12 13.5z"/><path d="M6.5 11v4.8c0 1.4 2.5 2.9 5.5 2.9s5.5-1.5 5.5-2.9V11"/><path d="M21.5 9v5"/>',
    "age": '<path d="M3.5 21h17"/><rect x="5" y="12" width="14" height="9" rx="1.8"/><path d="M5 16c1.2.9 2.3.9 3.5 0s2.3-.9 3.5 0 2.3.9 3.5 0 2.3-.9 3.5 0"/><path d="M12 12V8.5"/><path d="M12 6c.9-.8.9-1.8 0-2.8-.9 1-.9 2 0 2.8z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M20.5 20.5l-4.2-4.2"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "arrow": '<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>',
    "lock": '<rect x="5" y="11" width="14" height="9.5" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4.5 6h.01M4.5 12h.01M4.5 18h.01"/>',
}

TOOL_KEY = {
    "salary-tax-calculator": "tax", "govt-job-age-calculator": "age-job", "electricity-bill-calculator": "power",
    "zakat-calculator": "zakat", "percentage-calculator": "marks", "cgpa-calculator": "gpa", "age-calculator": "age",
}


def key(t):
    return TOOL_KEY[t["slug"]]


def card(t, extra=""):
    find = html.escape((t["short"] + " " + t["h1"] + " " + t["question"] + " " + t.get("keywords", "")).lower())
    return (f'<li data-tool="{key(t)}" data-find="{find}"{extra}><a class="card" href="/{t["slug"]}/">'
            f'<span class="top"><span class="ic">{svg(ICONS[key(t)])}</span><span class="name">{t["card_name"]}</span></span>'
            f'<span class="q">{t["question"]}</span>'
            f'<span class="foot"><span class="when">{t["when"]}</span><span class="go">Open {svg(ICONS["arrow"])}</span></span></a></li>')


def chips(active=None):
    items = "".join(
        f'<a class="chip" data-tool="{key(t)}" href="/{t["slug"]}/"{" aria-current=\"page\"" if t["slug"] == active else ""}>'
        f'{svg(ICONS[key(t)])}{t["short"]}</a>' for t in P.TOOLS)
    return f'<nav class="chips" aria-label="Calculators"><div class="wrap">{items}</div></nav>'


THEME_INIT = ("<script>try{var t=localStorage.getItem('hpk-theme');"
              "if(t)document.documentElement.setAttribute('data-theme',t)}catch(e){}</script>")


def url(slug):
    return P.BASE_URL + ("/" + slug + "/" if slug else "/")


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def head(pg, ld, body_attr=""):
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
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#16221c" media="(prefers-color-scheme: dark)">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/style.css?v={V}">
{THEME_INIT}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body{body_attr}>
<a class="skip-link" href="#main">Skip to content</a>
"""


def nav(active, tool=None, show_chips=True):
    links = [("", "Calculators", ""), ("about", "About", "hide-s"), ("contact", "Contact", "hide-xs")]
    items = "".join(
        f'<a href="{"/" + s + "/" if s else "/"}" class="{c}"{" aria-current=\"page\"" if s == active else ""}>{n}</a>'
        for s, n, c in links)
    return f"""<header class="site-nav"><div class="wrap bar">
<a class="logo" href="/" aria-label="{P.SITE_NAME} home">{LOGO}<span><span class="pk">Pak</span>Calculators</span></a>
<nav class="nav-links" aria-label="Main">{items}</nav>
</div>{chips(tool) if show_chips else ""}</header>
"""


def foot(scripts):
    tags = "".join(f'<script src="/assets/{s}?v={V}" defer></script>' for s in ["common.js"] + scripts)
    tools = "".join(f'<li><a href="/{t["slug"]}/">{t["card_name"]}</a></li>' for t in P.TOOLS)
    return f"""<footer class="site-foot"><div class="wrap">
<div class="cols">
<div><span class="brand">{LOGO}PakCalculators</span><p>Free calculators for everyday sums in Pakistan, built on the current official rules. Figures are estimates; check official sources for important decisions.</p></div>
<nav aria-label="Calculators"><h2>Calculators</h2><ul>{tools}</ul></nav>
<nav aria-label="Site"><h2>Site</h2><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="/privacy-policy/">Privacy policy</a></li><li><a href="/terms/">Terms and disclaimer</a></li></ul></nav>
</div>
<div class="legal"><p>© 2026 {P.SITE_NAME}</p><button type="button" class="theme-toggle" id="theme-toggle">Dark mode</button></div>
</div></footer>
{tags}
</body>
</html>
"""


def crumbs(pg):
    return (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / '
            f'<span aria-current="page">{html.escape(pg["short"])}</span></nav>')


def faq_html(faq):
    out = ['<h2 id="faq">Questions people ask</h2><div class="faq">']
    for q, a in faq:
        out.append(f"<details><summary>{q}</summary><div>{a}</div></details>")
    out.append("</div>")
    return "\n".join(out)


def related(pg):
    links = [t for t in P.TOOLS if t["slug"] != pg["slug"]][:3]
    items = "".join(card(t) for t in links)
    return f'<section class="related"><h2>More calculators</h2><ul class="cards c3">{items}</ul></section>'


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


def presets(pg):
    if not pg.get("presets"):
        return ""
    label, items = pg["presets"]
    btns = "".join(f'<button type="button" aria-pressed="false" data-fill="{html.escape(json.dumps(v))}">{html.escape(t)}</button>' for t, v in items)
    return f'<div class="presets" role="group" aria-label="{html.escape(label)}"><span class="pl">{html.escape(label)}</span>{btns}</div>\n'


def tool_page(pg):
    k = key(pg)
    body = f"""{nav(None, pg["slug"])}<main id="main" class="page">
<div class="tool-band"><div class="wrap">
{crumbs(pg)}
<header class="tool-head">
<span class="badge">{svg(ICONS[k])}</span>
<h1>{pg["h1"]}</h1>
<p class="checked">{svg(ICONS["check"])}{pg.get("checked_label", "Rates checked")} {P.CHECKED}</p>
</header>
</div></div>
<div class="wrap">
<div class="calc">
<form id="calc-form" class="panel" novalidate autocomplete="off">
{presets(pg)}{pg["form"]}
</form>
<aside class="slip" id="result" aria-live="polite"><p class="slip-title">Result</p><div class="slip-body"><p class="empty">Loading the calculator…</p></div></aside>
</div>
<div class="result-bar off" id="result-bar" hidden><div><span class="rb-k"></span><span class="rb-v"></span></div><a href="#result">See details</a></div>
<div class="article">
<p class="intro">{pg["lede"]}</p>
{pg["article"]}
{faq_html(pg["faq"])}
<h2>Sources</h2>
<p class="sources">{pg["sources"]}</p>
</div>
{related(pg)}
</div></main>
"""
    return head(pg, tool_ld(pg), f' data-tool="{k}"') + body + foot(pg["scripts"])


def info_page(pg):
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": pg["title"], "url": url(pg["slug"])}
    body = f"""{nav(pg["slug"])}<main id="main" class="page page-plain"><div class="wrap">
<div class="article">
<h1>{pg["h1"]}</h1>
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
    cards = "".join(card(t) for t in P.TOOLS)
    why = "".join(f'<li><span class="ic">{svg(ICONS[i])}</span><strong>{h}</strong><span>{b}</span></li>' for i, h, b in pg["why"])
    body = f"""{nav("", show_chips=False)}<main id="main">
<section class="hero"><div class="wrap">
<div class="hero-art" aria-hidden="true">
<div class="mini" data-tool="tax"><span class="mk"><i>{svg(ICONS["tax"])}</i>Tax on Rs 2.5 lakh salary</span><span class="mv">Rs 23,000 a month</span></div>
<div class="mini" data-tool="power"><span class="mk"><i>{svg(ICONS["power"])}</i>Bill for 300 units</span><span class="mv">Rs 13,450</span></div>
<div class="mini" data-tool="age-job"><span class="mk"><i>{svg(ICONS["age-job"])}</i>FPSC age limit</span><span class="mv">Eligible ✓</span></div>
</div>
<h1>{pg["h1"]}</h1>
<p class="lede">{pg["lede"]}</p>
<div class="finder">{svg(ICONS["search"])}<label for="tool-search" class="skip-link">Search calculators</label>
<input id="tool-search" type="search" placeholder="Search: tax, bill, zakat, age…" autocomplete="off"></div>
<ul class="trust"><li>{svg(ICONS["check"])}Free, no signup</li><li>{svg(ICONS["check"])}Updated for 2026-27</li><li>{svg(ICONS["check"])}Works on any phone</li></ul>
</div></section>
<div class="wrap">
<section class="home-tools" aria-label="All calculators">
<ul class="cards c3" id="tool-list">{cards}</ul>
<p class="none" id="no-match" hidden>No calculator matches that search yet. Try "tax", "bill" or "age", or <a href="/contact/">suggest a new calculator</a>.</p>
</section>
<div class="section-head" data-tool="tax"><h2>Quick tax check</h2><p>See the tax on your salary for 2026-27.</p></div>
<div class="quick" data-tool="tax">
<form id="calc-form" class="panel" novalidate autocomplete="off">
<div class="field"><label for="salary">Your monthly salary</label>
<div class="money"><span>Rs</span><input id="salary" type="text" inputmode="numeric" placeholder="150,000" value="150000"></div>
<input type="radio" name="period" value="month" checked hidden></div>
<p class="hint" style="margin:0"><a href="/salary-tax-calculator/">Open the full tax calculator</a> to see slabs, yearly figures and examples.</p>
</form>
<aside class="slip" id="result" aria-live="polite" data-compact></aside>
</div>
<div class="section-head"><h2>Why people use PakCalculators</h2></div>
<ul class="why">{why}</ul>
</div></main>
"""
    return head(pg, ld) + body + foot(["tools/salary-tax.js"])


def not_found():
    pg = {"slug": "404", "title": "Page not found | " + P.SITE_NAME, "description": "This page does not exist.", "noindex": True}
    rows = "".join(card(t) for t in P.TOOLS)
    body = f"""{nav(None)}<main id="main" class="page page-plain"><div class="wrap">
<h1>This page doesn't exist</h1>
<p>The link may be old or mistyped. Pick a calculator instead:</p><ul class="cards c3">{rows}</ul>
</div></main>
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

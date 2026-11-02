# PakCalculators

Free calculators for everyday sums in Pakistan: salary tax (2026-27 slabs), electricity bills, zakat, government job age with FPSC/PPSC relaxation, marks percentage, CGPA and exact age.

Plain HTML, CSS and JavaScript. Everything runs in the browser.

## Editing

Page text lives in `scripts/pages.py`; the calculators live in `assets/tools/`.

```
python3 scripts/build.py   # regenerate every page, sitemap and robots.txt
node scripts/test.js       # check every calculator against worked examples
```

When rates change (a new budget, a new NEPRA tariff), update the numbers in the matching file in `assets/tools/`, update the page text and `CHECKED` date in `scripts/pages.py`, bump `ASSET_VERSION`, then rebuild and run the tests.

When a custom domain is bought, change `BASE_URL` in `scripts/pages.py` and rebuild.

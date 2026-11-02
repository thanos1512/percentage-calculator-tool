"""All page content for HisaabPK. Edit text here, then run: python3 scripts/build.py"""

SITE_NAME = "HisaabPK"
BASE_URL = "https://hisaabpk.vercel.app"   # change to the custom domain once bought
EMAIL = "businessfor1512@gmail.com"
CHECKED = "2 November 2026"
CHECKED_ISO = "2026-11-02"
ASSET_VERSION = "1"


def money_field(id_, label, hint="", value="", placeholder="0"):
    h = f'<span class="hint">{hint}</span>' if hint else ""
    return (f'<div class="field"><label for="{id_}">{label}</label><div class="money"><span>Rs</span>'
            f'<input id="{id_}" type="text" inputmode="numeric" placeholder="{placeholder}" value="{value}"></div>{h}</div>')


def num_field(id_, label, hint="", value="", step="1", mn="0", placeholder=""):
    h = f'<span class="hint">{hint}</span>' if hint else ""
    return (f'<div class="field"><label for="{id_}">{label}</label><input id="{id_}" type="number" inputmode="decimal" '
            f'step="{step}" min="{mn}" value="{value}" placeholder="{placeholder}">{h}</div>')


def seg(name, label, options, checked):
    opts = "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{t}</span></label>'
        for v, t in options)
    return f'<div class="field"><span class="label" id="{name}-l">{label}</span><div class="seg" role="radiogroup" aria-labelledby="{name}-l">{opts}</div></div>'


def table(head, rows, num_cols=()):
    th = "".join(f'<th{" class=n" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(head))
    trs = "".join("<tr>" + "".join(f'<td{" class=n" if i in num_cols else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


# ---------------------------------------------------------------- Salary tax
SALARY = {
    "slug": "salary-tax-calculator",
    "short": "Salary tax",
    "question": "How much income tax comes out of my salary each month?",
    "when": "Finance Act 2026",
    "title": "Salary Tax Calculator Pakistan 2026-27 (New FBR Slabs)",
    "description": "Work out the income tax on your salary for 2026-27 with the new FBR slabs. See monthly tax, take-home pay and how much you save compared with last year.",
    "h1": "Salary tax calculator for 2026-27",
    "lede": "Enter your salary to see the income tax deducted each month under the new slabs, your take-home pay, and how it compares with last year.",
    "checked_label": "Slabs checked",
    "scripts": ["tools/salary-tax.js"],
    "form": money_field("salary", "Your salary", "Taxable salary before tax: basic pay plus taxable allowances.", "", "150,000")
            + seg("period", "This amount is per", [("month", "Month"), ("year", "Year")], "month"),
    "article": f"""
<h2>The new tax slabs for salaried people</h2>
<p>These slabs apply to salary paid from 1 July 2026 to 30 June 2027, which FBR calls tax year 2027. They come from the Finance Act 2026, which became law in late June 2026.</p>
{table(["Annual taxable salary", "Tax"], [
    ["Up to Rs 600,000", "No tax"],
    ["Rs 600,001 to 1,200,000", "1% of the amount above Rs 600,000"],
    ["Rs 1,200,001 to 2,200,000", "Rs 6,000 + 11% of the amount above Rs 1,200,000"],
    ["Rs 2,200,001 to 3,200,000", "Rs 116,000 + 20% of the amount above Rs 2,200,000"],
    ["Rs 3,200,001 to 4,100,000", "Rs 316,000 + 25% of the amount above Rs 3,200,000"],
    ["Rs 4,100,001 to 5,600,000", "Rs 541,000 + 29% of the amount above Rs 4,100,000"],
    ["Rs 5,600,001 to 7,000,000", "Rs 976,000 + 32% of the amount above Rs 5,600,000"],
    ["Above Rs 7,000,000", "Rs 1,424,000 + 35% of the amount above Rs 7,000,000"],
])}
<p>The 9% surcharge that applied to salaries above Rs 10 million a year in 2025-26 has been removed.</p>

<h2>How the tax is worked out</h2>
<p>Pakistan taxes salary in slabs. Only the part of your salary inside a slab is taxed at that slab's rate, so moving into a higher slab never makes your whole salary taxed at the higher rate.</p>
<ol>
<li>Multiply your monthly taxable salary by 12 to get the annual figure.</li>
<li>Find the slab your annual salary falls in.</li>
<li>Take the fixed amount for that slab, then add the slab's rate on the part of your salary above the slab's starting point.</li>
<li>Divide the annual tax by 12. That is roughly what your employer deducts each month.</li>
</ol>
<div class="example"><p><strong>Example: Rs 250,000 a month.</strong> The annual salary is Rs 3,000,000, which falls in the Rs 2.2 to 3.2 million slab. The tax is Rs 116,000 plus 20% of Rs 800,000 (Rs 160,000), so Rs 276,000 a year or <strong>Rs 23,000 a month</strong>. Under last year's 23% rate the same salary paid Rs 25,000 a month.</p></div>

<h2>Monthly tax at common salaries</h2>
{table(["Monthly salary", "Tax per month (2026-27)", "Tax per month (2025-26)", "Take-home"], [
    ["Rs 50,000", "Rs 0", "Rs 0", "Rs 50,000"],
    ["Rs 80,000", "Rs 300", "Rs 300", "Rs 79,700"],
    ["Rs 100,000", "Rs 500", "Rs 500", "Rs 99,500"],
    ["Rs 150,000", "Rs 6,000", "Rs 6,000", "Rs 144,000"],
    ["Rs 200,000", "Rs 13,000", "Rs 13,500", "Rs 187,000"],
    ["Rs 250,000", "Rs 23,000", "Rs 25,000", "Rs 227,000"],
    ["Rs 300,000", "Rs 34,667", "Rs 38,833", "Rs 265,333"],
    ["Rs 500,000", "Rs 92,000", "Rs 106,750", "Rs 408,000"],
    ["Rs 1,000,000", "Rs 264,500", "Rs 307,108", "Rs 735,500"],
], num_cols=(1, 2, 3))}
<p>Salaries up to about Rs 183,000 a month (Rs 2.2 million a year) pay the same as last year, because only the rates above Rs 2.2 million were cut.</p>

<h2>What counts as taxable salary</h2>
<p>Taxable salary is your basic pay plus most allowances, such as house rent, conveyance and bonuses. Some payments are partly or fully exempt, such as medical allowance up to 10% of basic pay when your employer does not provide free treatment. Your payslip or HR department can tell you the taxable figure if you are unsure. Enter that figure here for the closest estimate.</p>
<p>If you joined or left a job partway through the year, your employer spreads the annual tax over the months you work there, so the monthly deduction may differ from this estimate.</p>
""",
    "faq": [
        ("What is the tax-free salary limit in Pakistan for 2026-27?",
         "<p>Salary up to Rs 600,000 a year, which is Rs 50,000 a month, is not taxed.</p>"),
        ("How much tax will I pay on a salary of Rs 100,000 a month?",
         "<p>Rs 500 a month. Rs 100,000 a month is Rs 1.2 million a year, and 1% of the Rs 600,000 above the tax-free limit is Rs 6,000 a year.</p>"),
        ("Did the 2026-27 budget reduce salary tax?",
         "<p>Yes, for salaries above Rs 2.2 million a year (about Rs 183,000 a month). The rates for those slabs went down, and the surcharge on salaries above Rs 10 million was removed. Lower salaries pay the same as in 2025-26.</p>"),
        ("Does moving into a higher slab mean all my salary is taxed at the higher rate?",
         "<p>No. Only the part of your salary inside each slab is taxed at that slab's rate. A raise always leaves you with more money after tax.</p>"),
        ("Why is my employer deducting a different amount?",
         "<p>Your employer may be treating some allowances as exempt, adjusting for tax already deducted earlier in the year, or including a bonus. Ask HR for your tax computation if the difference is large.</p>"),
        ("Do I still need to file a tax return if tax is deducted from my salary?",
         "<p>If your taxable income is above the limit, filing a return keeps you on FBR's Active Taxpayer List, which lowers the withholding tax you pay on things like bank transactions, property and vehicle registration.</p>"),
    ],
    "sources": "Slabs from the Finance Act 2026 as reported by "
               '<a href="https://cssprep.com.pk/income-tax-slabs-2026-27-pakistan-salaried-class/" rel="nofollow">CSSPrep</a> and checked against the arithmetic of each slab; '
               'surcharge removal reported by <a href="https://pkrevenue.com/fbr-withdraws-9-percent-surcharge-salaried-persons/" rel="nofollow">PkRevenue</a>. '
               "For official figures, see the Income Tax Ordinance 2001, First Schedule, on fbr.gov.pk.",
}

# ---------------------------------------------------------------- Govt job age
FPSC_OPTS = """<div id="fpsc-opts">
<label class="check"><input type="checkbox" id="general" checked><span>Add the 5-year general relaxation <span class="hint">FPSC adds this on top of one other category.</span></span></label>
<div class="field"><label for="category">Other relaxation you qualify for</label>
<select id="category">
<option value="none">None</option>
<option value="area">AJK, Gilgit-Baltistan, tribal areas, Scheduled Caste or Buddhist (3 years)</option>
<option value="govt">Government servant with 2+ years service (10 years, up to 55)</option>
<option value="armed">Retired or released armed forces (years served, up to 15)</option>
<option value="deceased">Widow or child of a federal employee who died in service (5 years)</option>
</select></div>
<div id="served-field" hidden>""" + num_field("served", "Years served in the armed forces", "", "0") + """</div>
</div>
<div id="ppsc-opts" hidden>
<label class="check"><input type="checkbox" id="general-p" checked><span>Add the PPSC general relaxation <span class="hint">5 years for men, 8 years for women, unless the advert says otherwise.</span></span></label>
""" + seg("gender", "You are", [("m", "Male"), ("f", "Female")], "m") + num_field(
    "pb-service", "Punjab government service to exclude (years)", "Regular or contract service with the Punjab government is not counted in your age.", "0", "0.5") + """
</div>
<div id="other-opts" hidden>""" + num_field("custom-relax", "Relaxation stated in the advert (years)", "Add any relaxation the advert gives you.", "0") + """</div>
<label class="check"><input type="checkbox" id="inclusive"><span>Count the closing date as a full day <span class="hint">PPSC adds one day when it counts age. Switches on automatically for PPSC.</span></span></label>
"""

GOVT_AGE = {
    "slug": "govt-job-age-calculator",
    "short": "Govt job age",
    "question": "Am I within the age limit for this FPSC or PPSC post?",
    "when": "FPSC rules, July 2026",
    "category": "UtilitiesApplication",
    "title": "Age Calculator for Govt Jobs with FPSC & PPSC Age Relaxation",
    "description": "Check your exact age on a job advert's closing date and whether you are within the limit after FPSC or PPSC age relaxation. Shows the last date you stay eligible.",
    "h1": "Government job age calculator",
    "lede": "Find your exact age on the closing date of a job advert, add the age relaxation you qualify for, and see straight away whether you can apply.",
    "checked_label": "Rules checked",
    "scripts": ["tools/age-core.js", "tools/govt-age.js"],
    "form": '<div class="row2"><div class="field"><label for="dob">Date of birth</label><input id="dob" type="date"><span class="hint">As written on your matric certificate.</span></div>'
            '<div class="field"><label for="closing">Last date to apply</label><input id="closing" type="date"><span class="hint">The closing date in the advert.</span></div></div>'
            '<div class="row2">' + num_field("min-age", "Minimum age in the advert", "", "18") + num_field("max-age", "Maximum age in the advert", "Before any relaxation.", "25") + "</div>"
            + seg("commission", "Who is recruiting?", [("fpsc", "FPSC / federal"), ("ppsc", "PPSC / Punjab"), ("other", "Other")], "fpsc")
            + FPSC_OPTS,
    "article": f"""
<h2>How age is counted for government jobs</h2>
<p>Both FPSC and PPSC count your age on the <strong>closing date</strong> of the advertisement, not the date you apply or the test date. Your date of birth is taken from your matriculation certificate or its equivalent. For competitive exams such as CSS and PMS, the commission sets a fixed cut-off date in the exam notice instead.</p>
<p>An upper age limit of 30 years means you can apply until you complete 31 years. Someone aged 30 years, 11 months and 20 days is still within a 30-year limit. The calculator shows the exact last closing date you remain eligible for.</p>
<p>PPSC adds one day when it counts age. Its own example: a candidate born on 15 August 1970 was 27 years, 5 months and 24 days old on a closing date of 7 February 1998. Tick "Count the closing date as a full day" to use this method. It only matters if you are within a day or two of a limit.</p>

<h2>FPSC age relaxation</h2>
<p>FPSC applies the Initial Appointment to Civil Posts (Relaxation of Upper Age Limit) Rules, 1993. You can claim <strong>one</strong> of the categories below, plus the 5-year general relaxation on top.</p>
{table(["Category", "Extra years"], [
    ["General relaxation, for everyone", "5"],
    ["Permanent residents of AJK or Gilgit-Baltistan, recognised tribes of tribal areas, Scheduled Castes and the Buddhist community", "3"],
    ["Government servants, including contract employees, with 2 years of continuous service on the closing date", "10, up to a maximum age of 55"],
    ["Retired or released armed forces officers and personnel", "Years actually served, up to 15"],
    ["Widow, son or daughter of a federal civil servant who died in service", "5"],
], num_cols=(1,))}
<p>Employees of nationalised banks, the State Bank, WAPDA and other autonomous or semi-government bodies do not count as government servants for this relaxation. You need proof of the category you claim, such as a departmental permission certificate or a domicile-based certificate.</p>
<div class="example"><p><strong>Example.</strong> An advert for a BS-16 post sets the age limit at 18 to 25 and closes on 20 November 2026. A candidate born on 10 March 1996 is 30 years, 8 months and 10 days old that day. With the 5-year general relaxation the limit becomes 30, so they can apply. They stay eligible for adverts closing up to 9 March 2027, the day before their 31st birthday.</p></div>

<h2>PPSC age relaxation</h2>
<p>PPSC's own guidance gives a general relaxation of 5 years for men and 8 years for women for posts where the candidate meets the other requirements. Time spent in regular or contract service with the Punjab government is also left out when counting age, but the total cannot go above 35 for Combined Competitive Examination posts. Relaxation for federal or autonomous-body employees applies only if the advert says so.</p>
<p>Punjab sometimes grants one-off relaxations too. For example, it allowed PMS candidates up to age 32 for the 2026 and 2027 exams. Always read the advert for the post you are applying to.</p>

<h2>Other commissions and departments</h2>
<p>KPPSC, SPSC, BPSC, AJK PSC and departments that recruit directly (FIA, police, WAPDA and others) publish their own limits and relaxations in each advert. Choose "Other" and enter the relaxation the advert gives you.</p>
""",
    "faq": [
        ("Is age counted on the closing date or the test date?",
         "<p>On the closing date of the advertisement for FPSC and PPSC posts. Competitive exams like CSS and PMS use a fixed cut-off date stated in the exam notice.</p>"),
        ("If the upper age limit is 30, can I apply at 30 years and 6 months?",
         "<p>Yes. You stay within a 30-year limit until you complete 31 years. The calculator shows the exact last closing date you can apply for.</p>"),
        ("Can I combine two FPSC age relaxations?",
         "<p>You can combine the 5-year general relaxation with one other category. If you qualify for two other categories, such as government service and AJK domicile, you get the larger one only.</p>"),
        ("Does the general age relaxation apply to CSS?",
         "<p>CSS has its own age rules in the annual CSS notice, so check that notice rather than the general recruitment rules.</p>"),
        ("Which date of birth is used?",
         "<p>The one on your matriculation (SSC) or O-Level certificate. If that certificate has no date of birth, commissions accept a school leaving certificate with a birth certificate or CNIC.</p>"),
        ("I'm a government employee. How much relaxation do I get from FPSC?",
         "<p>Up to 10 years, as long as your total age stays at or below 55 and you have 2 years of continuous government service on the closing date. The 5-year general relaxation is added on top, still within the 55 cap.</p>"),
    ],
    "sources": 'FPSC <a href="https://fpsc.gov.pk/uploads/content/1785140430996_Instructions_to_the_candidates_-_updated_on_23.7.2026.pdf" rel="nofollow">Instructions to the candidates</a> (updated 23 July 2026); '
               'PPSC <a href="https://ppsc.gop.pk/" rel="nofollow">frequently asked questions</a>; '
               'Punjab PMS relaxation as reported by <a href="https://www.ilmkidunya.com/edunews/punjab-announces-major-age-relief-for-pms-candidates" rel="nofollow">Ilmkidunya</a> (August 2026).',
}

# ---------------------------------------------------------------- Electricity
ELECTRICITY = {
    "slug": "electricity-bill-calculator",
    "short": "Electricity bill",
    "question": "What will my bill be for the units I used?",
    "when": "Tariff from Feb 2026",
    "title": "Electricity Bill Calculator Pakistan 2026 (LESCO, IESCO, MEPCO & All)",
    "description": "Estimate your electricity bill from the units used, with the current per-unit rates, fixed charges, FC surcharge and GST. Works for LESCO, IESCO, GEPCO, FESCO, MEPCO and all DISCOs.",
    "h1": "Electricity bill calculator",
    "lede": "Enter the units you used to estimate your home electricity bill, with the current slab rates, fixed charges and taxes. The same rates apply to LESCO, IESCO, GEPCO, FESCO, MEPCO, PESCO, HESCO and the other companies.",
    "checked_label": "Tariff checked",
    "scripts": ["tools/electricity.js"],
    "form": num_field("units", "Units used this month", "Printed on your bill as units consumed.", "", "1", "0", "250")
            + seg("type", "Your consumer type", [("non", "Non-protected"), ("protected", "Protected"), ("lifeline", "Lifeline")], "non")
            + '<p class="hint" style="margin-top:-.6rem">Protected means you used 200 units or fewer in each of the last 6 months. Lifeline means 100 units or fewer.</p>'
            + '<div class="row2">' + num_field("load", "Sanctioned load (kW)", "Printed on your bill. Most homes have 1 to 5 kW.", "1", "1", "1")
            + num_field("fpa", "Fuel adjustment per unit (Rs)", "Optional. Use a minus sign for a refund.", "", "0.01", "-20", "0") + "</div>"
            + '<label class="check"><input type="checkbox" id="duty" checked><span>Include electricity duty (1.5%)</span></label>'
            + '<label class="check"><input type="checkbox" id="tv"><span>Include PTV fee (Rs 35)</span></label>'
            + '<label class="check"><input type="checkbox" id="nonfiler"><span>I am not on FBR\'s Active Taxpayer List <span class="hint">Adds 7.5% income tax on bills above Rs 25,000.</span></span></label>',
    "article": f"""
<h2>Per-unit rates for homes</h2>
<p>NEPRA sets one national tariff for household electricity, so every distribution company bills homes at the same base rates. These are the rates notified in February 2026.</p>
{table(["Units used in the month", "Non-protected (Rs/unit)", "Fixed charge (Rs/kW)"], [
    ["1 to 100", "22.44", "275"], ["101 to 200", "28.91", "300"], ["201 to 300", "33.10", "350"],
    ["301 to 400", "36.46", "400"], ["401 to 500", "38.95", "500"], ["501 to 600", "40.22", "675"],
    ["601 to 700", "41.85", "675"], ["Above 700", "47.20", "675"],
], num_cols=(1, 2))}
{table(["Protected and lifeline homes", "Rs/unit", "Fixed charge (Rs/kW)"], [
    ["Protected, 1 to 100 units", "10.54", "200"], ["Protected, 101 to 200 units", "13.01", "300"],
    ["Lifeline, up to 50 units", "3.95", "none"], ["Lifeline, 51 to 100 units", "7.74", "none"],
], num_cols=(1, 2))}

<h2>How your bill is calculated</h2>
<p><strong>Non-protected homes</strong> pay one rate on every unit: the rate of the slab their total falls in. At 250 units, all 250 units are charged at Rs 33.10.</p>
<p><strong>Protected homes</strong> get the benefit of the lower slab. At 150 units, the first 100 units are charged at Rs 10.54 and the other 50 at Rs 13.01.</p>
<p>On top of the energy charge, the bill adds:</p>
<ul>
<li><strong>Fixed charges</strong>, multiplied by your sanctioned load in kW. These were introduced for homes in 2026.</li>
<li><strong>Financing cost (FC) surcharge</strong>: Rs 3.23 per unit, or Rs 1.43 per unit for protected homes.</li>
<li><strong>Fuel price adjustment (FPA)</strong>: changes every month and can be a charge or a refund. Enter it if you know this month's figure.</li>
<li><strong>Electricity duty</strong>: a provincial levy of about 1.5%. Some provinces have stopped charging it, so untick it if your bill shows none.</li>
<li><strong>GST of 18%</strong> on the charges above.</li>
<li><strong>Income tax</strong> of 7.5% if the bill is above Rs 25,000 and you are not on the Active Taxpayer List.</li>
</ul>

<h2>The 200-unit line</h2>
<p>Crossing 200 units costs a protected home far more than one extra unit. At 200 units a protected home with 2 kW load pays about Rs 3,866. At 201 units the whole bill moves to the non-protected 201 to 300 slab and comes to about Rs 9,561, and the home loses protected status for the next six months. The calculator warns you when you are just above a slab line and shows how much you would save by staying below it.</p>

<h2>Example bills</h2>
<p>For a home with 2 kW sanctioned load, including electricity duty and GST, with no fuel adjustment:</p>
{table(["Units", "Type", "Estimated bill"], [
    ["100", "Protected", "Rs 1,903"], ["200", "Protected", "Rs 3,866"], ["200", "Non-protected", "Rs 8,395"],
    ["201", "Non-protected", "Rs 9,561"], ["300", "Non-protected", "Rs 13,863"], ["301", "Non-protected", "Rs 15,235"],
    ["500", "Non-protected", "Rs 26,411"],
], num_cols=(0, 2))}
<p>Your real bill can differ because of the monthly fuel adjustment, quarterly adjustments, arrears, and any provincial charges. Use this as a guide to the size of the bill and the effect of using fewer units.</p>
""",
    "faq": [
        ("Are LESCO, IESCO and MEPCO rates different?",
         "<p>No. Household rates are set nationally by NEPRA, so LESCO, IESCO, GEPCO, FESCO, MEPCO, PESCO, HESCO, SEPCO, QESCO and TESCO all use the same per-unit rates. Monthly fuel adjustments can differ slightly, and K-Electric publishes its own adjustments.</p>"),
        ("What does protected consumer mean?",
         "<p>A home that used 200 units or fewer in each of the last six months. Protected homes pay much lower rates. Using more than 200 units in any month removes the status for the next six months.</p>"),
        ("Why did my bill jump after 200 units?",
         "<p>Above 200 units you are billed at non-protected rates, and all your units are charged at the slab rate your total falls in. One unit over 200 can more than double the bill.</p>"),
        ("What are the fixed charges on my bill?",
         "<p>Since 2026, household bills include a monthly fixed charge per kW of sanctioned load, from Rs 200 to Rs 675 per kW depending on your slab. Lifeline homes pay none.</p>"),
        ("Where do I find my sanctioned load?",
         "<p>It is printed near the top of your bill, usually as Sanctioned Load or Load (kW).</p>"),
        ("How accurate is this estimate?",
         "<p>It uses the notified rates and the standard taxes, so it should be close for the energy part of the bill. Items that change each month, like the fuel price adjustment, arrears and quarterly adjustments, will make your actual bill differ.</p>"),
    ],
    "sources": 'Rates from S.R.O. 279(I)/2026 as summarised by <a href="https://www.toolsfluent.com/blog/electricity-slab-rates-pakistan-2026" rel="nofollow">ToolsFluent</a>; '
               'fixed charges reported by <a href="https://www.geo.tv/latest/650317-nepra-imposes-fixed-charges-on-consumers-using-up-to-300-units" rel="nofollow">Geo News</a>; '
               'slab billing method from the SRO as explained on <a href="https://dev.to/lowkeybuilds/the-201st-unit-modelling-pakistans-2026-electricity-slab-tariff-from-a-scanned-sro-32ha" rel="nofollow">DEV Community</a>. '
               "Official tariffs are published on nepra.org.pk.",
}

# ---------------------------------------------------------------- Zakat
ZAKAT = {
    "slug": "zakat-calculator",
    "short": "Zakat",
    "question": "How much zakat do I owe on my savings, gold and silver?",
    "when": "Enter today's prices",
    "title": "Zakat Calculator Pakistan 2026: Gold, Silver, Cash & Nisab",
    "description": "Calculate zakat on cash, bank savings, gold, silver and business stock in rupees. Uses the silver or gold nisab with today's price per tola, and 2.5% of zakatable wealth.",
    "h1": "Zakat calculator",
    "lede": "Add up your cash, savings, gold, silver and business stock to see whether zakat is due and how much to pay. Enter today's gold and silver price per tola from your local market.",
    "checked_label": "Method checked",
    "scripts": ["tools/zakat.js"],
    "form": seg("unit", "Weigh gold and silver in", [("tola", "Tola"), ("g", "Grams")], "tola")
            + '<div class="row2">' + num_field("gold", "Gold you own", "", "", "0.01", "0", "0")
            + '<div class="field" id="gold-price-field"><label for="gold-price">Gold price per tola</label><div class="money"><span>Rs</span><input id="gold-price" type="text" inputmode="numeric" placeholder="Today\'s rate"></div><span class="hint" hidden>Enter the gold price to include your gold.</span></div></div>'
            + '<div class="row2">' + num_field("silver", "Silver you own", "", "", "0.01", "0", "0")
            + money_field("silver-price", "Silver price per tola", "Needed for the silver nisab.", "", "Today's rate") + "</div>"
            + money_field("cash", "Cash at home") + money_field("bank", "Bank and savings balances")
            + money_field("business", "Business stock for sale", "Value at today's selling price.")
            + money_field("receivable", "Money owed to you", "Loans you expect to get back.")
            + money_field("investments", "Shares, funds and prize bonds")
            + money_field("debts", "Debts and bills due now", "Subtracted from your wealth.")
            + seg("basis", "Nisab based on", [("silver", "Silver (52.5 tola)"), ("gold", "Gold (7.5 tola)")], "silver"),
    "article": f"""
<h2>How zakat is calculated</h2>
<ol>
<li>Add up the zakatable wealth you own: cash, bank balances, gold, silver, goods held for sale, money owed to you that you expect back, and investments.</li>
<li>Subtract debts and bills that are due now.</li>
<li>Compare the result with the nisab. If it is equal to or more than the nisab, and has stayed so for a full lunar year, zakat is due.</li>
<li>Zakat is 2.5% of the total, which is the same as dividing by 40.</li>
</ol>
<p>You do not pay zakat on your home, your car, furniture, clothes or the tools you use for work.</p>

<h2>Nisab: the threshold for zakat</h2>
{table(["Basis", "Weight", "In grams"], [
    ["Silver", "52.5 tola", "612.35 g"], ["Gold", "7.5 tola", "87.48 g"],
], num_cols=(1, 2))}
<p>Because silver is far cheaper than gold, the silver nisab is much lower, so more people owe zakat under it. Most scholars in Pakistan advise using the silver nisab when your wealth is a mix of cash, savings and gold, because it benefits more of the poor. If all your zakatable wealth is gold and nothing else, many scholars apply the gold nisab instead. If you are unsure which applies to you, ask a scholar you trust.</p>
<p>For deduction from bank accounts on the first of Ramadan 2026, the government set the nisab at Rs 503,529. Banks use that fixed figure for the whole year, but for your own calculation use today's silver price.</p>

<h2>Example</h2>
<div class="example"><p>Ahmed has Rs 300,000 in the bank, Rs 50,000 cash at home and 2 tola of gold, with gold at Rs 400,000 a tola and silver at Rs 9,600 a tola. He owes Rs 30,000 on a bill due now. His zakatable wealth is Rs 300,000 + Rs 50,000 + Rs 800,000 − Rs 30,000 = Rs 1,120,000. The silver nisab is 52.5 × Rs 9,600 = Rs 504,000, so zakat is due: 2.5% of Rs 1,120,000 is <strong>Rs 28,000</strong>.</p></div>

<h2>Gold and silver in tola and grams</h2>
<p>One tola is 11.6638 grams. Jewellers in Pakistan quote prices per tola, and often per 10 grams. If your jewellery is 22 or 21 carat, use the price for that purity, since it is lower than the 24-carat price.</p>
""",
    "faq": [
        ("What is the zakat nisab in Pakistan in 2026?",
         "<p>The nisab is the value of 52.5 tola of silver, or 7.5 tola of gold. Its rupee value changes with the market. For bank deductions in Ramadan 2026 the government fixed it at Rs 503,529.</p>"),
        ("Should I use the gold or silver nisab?",
         "<p>Most scholars in Pakistan advise silver when you own a mix of cash, savings and gold. If you own only gold, many apply the gold nisab. Ask a scholar if you are unsure.</p>"),
        ("Is zakat due on gold jewellery that I wear?",
         "<p>In the Hanafi school, followed by most people in Pakistan, zakat is due on gold and silver jewellery even if it is worn. Other schools differ on this.</p>"),
        ("How do I calculate zakat on 1 tola of gold?",
         "<p>Multiply 1 tola by today's price per tola to get its value, add your other zakatable wealth, and if the total is above the nisab, pay 2.5% of the total.</p>"),
        ("Do I pay zakat on my house or car?",
         "<p>No. Zakat is not due on the home you live in, your car, household items or tools for your work. A property or car bought to sell is business stock and is counted.</p>"),
        ("My bank already deducted zakat. Do I pay again?",
         "<p>The bank deduction counts towards your zakat on that account. Calculate your full zakat and subtract what the bank already took.</p>"),
    ],
    "sources": 'Ramadan 2026 bank nisab as reported by <a href="https://profit.pakistantoday.com.pk/2026/02/17/pakistan-fixes-zakat-nisab-at-rs503529-for-ramadan-2026/" rel="nofollow">Profit by Pakistan Today</a>. '
               "Nisab weights and the 2.5% rate are the standard figures used by scholars in Pakistan.",
}

# ---------------------------------------------------------------- Percentage
PERCENTAGE = {
    "slug": "percentage-calculator",
    "short": "Marks percentage",
    "question": "What percentage and grade did I get in my exam?",
    "when": "IBCC grading",
    "category": "EducationalApplication",
    "title": "Percentage Calculator for Marks with Matric & Inter Grade",
    "description": "Turn obtained marks into a percentage and see your grade on both the new IBCC scale (A++ to U) and the old board scale. Also works out any percentage of a number.",
    "h1": "Marks percentage calculator",
    "lede": "Enter your obtained and total marks to get your percentage, your grade on the new and old board scales, and the marks you need for the next grade.",
    "checked_label": "Grades checked",
    "scripts": ["tools/percentage.js"],
    "form": '<div class="row2">' + num_field("obtained", "Obtained marks", "", "", "0.5", "0", "1020")
            + num_field("total", "Total marks", "Matric and inter are usually out of 1200.", "1200", "1", "1") + "</div>",
    "article": f"""
<h2>How to calculate percentage from marks</h2>
<p>Divide your obtained marks by the total marks and multiply by 100.</p>
<div class="example"><p><strong>Example.</strong> 1020 marks out of 1200: 1020 ÷ 1200 = 0.85, and 0.85 × 100 = <strong>85%</strong>. On the new IBCC scale that is grade A.</p></div>

<h2>Other percentage sums</h2>
<div class="panel" style="margin-bottom:1.5rem">
<form id="quick-form" novalidate autocomplete="off">
<div class="row3"><div class="field"><label for="q1a">What is</label><input id="q1a" type="number" inputmode="decimal" placeholder="15" value="15"></div>
<div class="field"><label for="q1b">% of</label><input id="q1b" type="number" inputmode="decimal" placeholder="2,000" value="2000"></div>
<div class="field"><span class="label">Answer</span><output id="q1r" for="q1a q1b" style="display:block;font-size:1.3rem;font-weight:700;padding:.5rem 0">300</output></div></div>
<div class="row3"><div class="field"><label for="q2a">What % is</label><input id="q2a" type="number" inputmode="decimal" placeholder="45" value="45"></div>
<div class="field"><label for="q2b">of</label><input id="q2b" type="number" inputmode="decimal" placeholder="60" value="60"></div>
<div class="field"><span class="label">Answer</span><output id="q2r" for="q2a q2b" style="display:block;font-size:1.3rem;font-weight:700;padding:.5rem 0">75%</output></div></div>
<div class="row3"><div class="field"><label for="q3a">Change from</label><input id="q3a" type="number" inputmode="decimal" placeholder="80" value="80"></div>
<div class="field"><label for="q3b">to</label><input id="q3b" type="number" inputmode="decimal" placeholder="100" value="100"></div>
<div class="field"><span class="label">Answer</span><output id="q3r" for="q3a q3b" style="display:block;font-size:1.3rem;font-weight:700;padding:.5rem 0">+25%</output></div></div>
</form></div>

<h2>New grading system for matric and inter</h2>
<p>The Inter Board Committee of Chairmen (IBCC) introduced a new grading scale for SSC and HSSC, phased in from 2023, and raised the pass mark from 33% to 40%. The Federal Board, Sindh boards, AJK Mirpur, Karakoram, AKU-EB and others have started using it.</p>
{table(["Percentage", "Grade", "Remarks"], [
    ["95% to 100%", "A++", "Exceptional"], ["90% to 94%", "A+", "Outstanding"], ["85% to 89%", "A", "Excellent"],
    ["80% to 84%", "B++", "Very good"], ["75% to 79%", "B+", "Good"], ["70% to 74%", "B", "Fairly good"],
    ["60% to 69%", "C", "Above average"], ["50% to 59%", "D", "Average"], ["40% to 49%", "E", "Below average"],
    ["Below 40%", "U", "Unsatisfactory"],
])}
<h2>Old grading system</h2>
<p>Some boards still print grades on the older scale, where the pass mark is 33%.</p>
{table(["Percentage", "Grade"], [
    ["80% and above", "A+"], ["70% to 79%", "A"], ["60% to 69%", "B"], ["50% to 59%", "C"],
    ["40% to 49%", "D"], ["33% to 39%", "E"], ["Below 33%", "F (fail)"],
])}
""",
    "faq": [
        ("How do I calculate my matric percentage?",
         "<p>Divide your obtained marks by the total marks (usually 1200) and multiply by 100. For example, 960 out of 1200 is 80%.</p>"),
        ("What grade is 85% in the new system?",
         "<p>Grade A, described as excellent. 90% and above is A+, and 95% and above is A++.</p>"),
        ("What is the passing percentage in matric and inter now?",
         "<p>Under the new IBCC policy the pass mark is 40%. Boards still on the old system use 33%.</p>"),
        ("How many marks out of 1200 do I need for A+?",
         "<p>For A+ on the new scale you need 90%, which is 1080 out of 1200. On the old scale A+ starts at 80%, which is 960 out of 1200.</p>"),
        ("How do I find 20% of a number?",
         "<p>Multiply the number by 20 and divide by 100. For example, 20% of 5,000 is 1,000. The quick calculator on this page does it for you.</p>"),
    ],
    "sources": 'IBCC grading table from the <a href="https://ibcc.edu.pk/faq_cat/new-grading-system-of-ssc-hssc/page/3/" rel="nofollow">IBCC new grading system FAQ</a>; '
               'boards adopting it as reported by <a href="https://tribune.com.pk/story/2627671/new-policy-sets-40-minimum-passing-marks" rel="nofollow">The Express Tribune</a> (September 2026).',
}

# ---------------------------------------------------------------- CGPA
CGPA = {
    "slug": "cgpa-calculator",
    "short": "GPA and CGPA",
    "question": "What is my semester GPA and new CGPA?",
    "when": "4.00 scale",
    "category": "EducationalApplication",
    "title": "CGPA Calculator for Pakistani Universities (4.00 Scale)",
    "description": "Calculate your semester GPA from course grades and credit hours, then your new CGPA. Uses the 4.00 grade-point scale followed by most HEC-recognised universities.",
    "h1": "GPA and CGPA calculator",
    "lede": "Add your courses with their credit hours and grades to get your semester GPA. Enter your current CGPA too, and you'll see your new CGPA.",
    "checked_label": "Scale checked",
    "scripts": ["tools/cgpa.js"],
    "form": '<div id="courses" class="courses"></div>'
            '<p><button type="button" class="ghost" id="add-course">Add a course</button></p>'
            '<h3 style="margin-top:1.4rem">Already have a CGPA? <span class="hint" style="display:inline;font-weight:400">Optional</span></h3>'
            '<div class="row2">' + num_field("prev-cgpa", "Current CGPA", "", "", "0.01", "0", "3.20")
            + num_field("prev-credits", "Credit hours completed", "Before this semester.", "", "1", "0", "60") + "</div>",
    "article": f"""
<h2>How GPA is calculated</h2>
<p>Each grade carries grade points. Multiply each course's grade points by its credit hours to get quality points, add them up, and divide by the total credit hours.</p>
<div class="example"><p><strong>Example.</strong> A in a 3-credit course (3 × 4.00 = 12), B+ in a 3-credit course (3 × 3.33 = 9.99) and B in a 2-credit lab (2 × 3.00 = 6). Quality points: 27.99. Credit hours: 8. GPA = 27.99 ÷ 8 = <strong>3.49</strong>.</p></div>

<h2>How CGPA is calculated</h2>
<p>CGPA is the GPA across every semester, weighted by credit hours. Multiply your current CGPA by the credit hours you have completed, add this semester's quality points, and divide by the new total of credit hours.</p>
<div class="example"><p><strong>Example.</strong> CGPA 3.20 over 60 credit hours, then a semester GPA of 3.60 over 18 credit hours: (3.20 × 60 + 3.60 × 18) ÷ 78 = 256.8 ÷ 78 = <strong>3.29</strong>.</p></div>

<h2>Grade points on the 4.00 scale</h2>
{table(["Grade", "Grade points"], [
    ["A", "4.00"], ["A-", "3.67"], ["B+", "3.33"], ["B", "3.00"], ["B-", "2.67"], ["C+", "2.33"],
    ["C", "2.00"], ["C-", "1.67"], ["D+", "1.33"], ["D", "1.00"], ["F", "0.00"],
], num_cols=(1,))}
<p>Most Pakistani universities use these grade points, but the percentage that earns each letter grade varies from one university to another. Check your university's prospectus or semester rules for its own table, and pick the grade whose points match.</p>
<p>This calculator cuts results to two decimals rather than rounding them up, as most universities do on transcripts. A GPA of 2.996 shows as 2.99.</p>
""",
    "faq": [
        ("What is the difference between GPA and CGPA?",
         "<p>GPA is for one semester. CGPA (cumulative GPA) covers every semester you have studied so far, weighted by credit hours.</p>"),
        ("What CGPA do I need to avoid probation?",
         "<p>Most universities place students on probation below 2.00 CGPA, and many require at least 2.00 to graduate with a bachelor's degree and 2.50 for a master's. Check your university's rules.</p>"),
        ("Do labs count in CGPA?",
         "<p>Yes, a lab with its own credit hours and grade counts like any other course, weighted by its credit hours.</p>"),
        ("Can I convert CGPA to percentage?",
         "<p>There is no single formula used by every university. Many publish their own conversion table on the transcript or in the prospectus, and HEC degree attestation uses the CGPA itself. Use your university's table.</p>"),
        ("How do repeated courses affect CGPA?",
         "<p>Most universities replace the old grade with the new one when you repeat a course. Leave the old attempt out and enter only the new grade.</p>"),
    ],
    "sources": "Grade points follow the 4.00 scale used by most HEC-recognised universities, for example the "
               '<a href="https://kkkuk.edu.pk/grading-system/" rel="nofollow">Khushal Khan Khattak University grading system</a>. '
               "Your own university's rules are final.",
}

# ---------------------------------------------------------------- Age
AGE = {
    "slug": "age-calculator",
    "short": "Age",
    "question": "How old am I exactly, in years, months and days?",
    "when": "Always current",
    "category": "UtilitiesApplication",
    "title": "Age Calculator: Exact Age in Years, Months and Days",
    "description": "Find your exact age in years, months and days from your date of birth, plus total days, weeks and the countdown to your next birthday.",
    "h1": "Age calculator",
    "lede": "Enter your date of birth to see your exact age in years, months and days, the day of the week you were born, and how long until your next birthday.",
    "checked_label": "Updated",
    "scripts": ["tools/age-core.js", "tools/age.js"],
    "form": '<div class="row2"><div class="field"><label for="dob">Date of birth</label><input id="dob" type="date"></div>'
            '<div class="field"><label for="on">Age on this date</label><input id="on" type="date"><span class="hint">Today, unless you change it.</span></div></div>',
    "article": """
<h2>How exact age is worked out</h2>
<p>The calculator counts whole years since your date of birth, then whole months after your last birthday, then the days left over. When the day of the month in your birth date is later than today's, it borrows the days of the previous month, which is how ages are counted on official forms.</p>
<div class="example"><p><strong>Example.</strong> Someone born on 15 August 2000 is 26 years, 2 months and 18 days old on 2 November 2026.</p></div>
<p>If you were born on 29 February, your birthday is taken as 28 February in years that are not leap years.</p>
<h2>Checking your age for a job advert</h2>
<p>Government job adverts count your age on the closing date and often allow age relaxation. Use the <a href="/govt-job-age-calculator/">government job age calculator</a> to check eligibility with FPSC or PPSC relaxation added.</p>
""",
    "faq": [
        ("How do I calculate my age from my date of birth?",
         "<p>Subtract your birth year from the current year, then take one off if your birthday has not come yet this year. For months and days, count whole months since your last birthday and the days left over. The calculator does all of this for you.</p>"),
        ("What day of the week was I born?",
         "<p>Enter your date of birth and the result shows the weekday you were born on.</p>"),
        ("Can I check my age on a past or future date?",
         "<p>Yes. Change the \"Age on this date\" field to any date.</p>"),
    ],
    "sources": "Calendar calculation; no external data is used.",
}

TOOLS = [SALARY, GOVT_AGE, ELECTRICITY, ZAKAT, PERCENTAGE, CGPA, AGE]

# ---------------------------------------------------------------- Home
HOME = {
    "slug": "",
    "title": "HisaabPK: Free Salary Tax, Bill, Zakat & Age Calculators for Pakistan",
    "description": "Free calculators for everyday sums in Pakistan: salary tax under the 2026-27 slabs, electricity bills, zakat, government job age limits, marks percentage and CGPA.",
    "h1": "Everyday sums for Pakistan, worked out",
    "lede": "Salary tax, electricity bills, zakat, job age limits and exam marks. Each calculator uses the current rules and shows every step, so you can check it yourself.",
    "body": """
<h2>Why these calculators</h2>
<p>Most calculators online are built for other countries. These are built around Pakistani rules: FBR's tax slabs, NEPRA's electricity tariff, FPSC and PPSC age relaxation, and board and university grading. Each page lists the date its figures were last checked and links to the sources.</p>
<p>Everything runs in your browser. Nothing you type is sent anywhere or stored.</p>
""",
}

# ---------------------------------------------------------------- Info pages
INFO = [
    {
        "slug": "about", "title": "About HisaabPK", "h1": "About HisaabPK",
        "description": "Who makes HisaabPK, where the figures come from, and how the calculators are checked.",
        "body": """
<p>HisaabPK is a set of free calculators for everyday money and paperwork questions in Pakistan. <em>Hisaab</em> means working out the sums, and that is all this site does: it takes the rules that affect you, like tax slabs, electricity tariffs and age limits, and applies them to your numbers.</p>
<h2>Where the figures come from</h2>
<p>Every calculator is based on official rules: the Finance Act and FBR for income tax, NEPRA's notified tariff for electricity, FPSC and PPSC instructions for age limits, and IBCC and university rules for grades. Each page shows when its figures were last checked and links to its sources. When a budget or tariff changes, the pages are updated.</p>
<h2>How the calculators are checked</h2>
<p>Every calculator is tested against worked examples, including examples published by the official bodies themselves, such as PPSC's own age calculation.</p>
<h2>A note on accuracy</h2>
<p>The results are estimates to help you plan. For decisions that matter, such as a tax return, a job application or a large zakat payment, confirm with the official source, your employer, or a scholar. See the <a href="/terms/">terms and disclaimer</a>.</p>
<p>Found a mistake or want a calculator added? <a href="/contact/">Get in touch</a>.</p>
""",
    },
    {
        "slug": "contact", "title": "Contact HisaabPK", "h1": "Contact",
        "description": "Report a mistake, suggest a calculator, or ask a question about HisaabPK.",
        "body": f"""
<p>If a figure looks wrong, a rule has changed, or there is a calculator you would like to see, email:</p>
<p><a href="mailto:{EMAIL}" style="font-size:1.2rem;font-weight:600">{EMAIL}</a></p>
<p>When reporting a mistake, include the page, the numbers you entered, and the result you expected. Replies usually take a few days.</p>
<p>HisaabPK cannot give personal tax, legal or religious advice. For those, please contact FBR, a tax adviser, the relevant commission, or a scholar.</p>
""",
    },
    {
        "slug": "privacy-policy", "title": "Privacy Policy | HisaabPK", "h1": "Privacy policy",
        "description": "How HisaabPK handles your information, cookies and advertising.",
        "body": f"""
<p>Last updated: {CHECKED}</p>
<h2>What you type into the calculators</h2>
<p>All calculations run in your own browser. The numbers and dates you enter are not sent to us or stored on any server. The only thing saved on your device is your light or dark mode choice, if you change it.</p>
<h2>Hosting and logs</h2>
<p>The site is hosted on Vercel. Like most web hosts, Vercel may record basic technical data such as IP address, browser type and the pages requested, for security and performance.</p>
<h2>Advertising and cookies</h2>
<p>This site may show ads from Google AdSense. Google and its partners use cookies to show ads based on your visits to this and other websites. You can turn off personalised ads at <a href="https://www.google.com/settings/ads" rel="nofollow">Google Ads Settings</a>, and learn more about how Google uses data at <a href="https://policies.google.com/technologies/partner-sites" rel="nofollow">policies.google.com/technologies/partner-sites</a>.</p>
<p>The site may also use analytics to count visits. These tools may use cookies, which you can block in your browser settings.</p>
<h2>Fonts</h2>
<p>Text is displayed with a font loaded from Google Fonts, which receives your IP address when the font is downloaded.</p>
<h2>Children</h2>
<p>The site is for a general audience and does not knowingly collect personal information from anyone.</p>
<h2>Contact</h2>
<p>Questions about this policy: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
""",
    },
    {
        "slug": "terms", "title": "Terms and Disclaimer | HisaabPK", "h1": "Terms and disclaimer",
        "description": "Terms of use and the disclaimer for HisaabPK's calculators.",
        "body": f"""
<p>Last updated: {CHECKED}</p>
<h2>Estimates, not advice</h2>
<p>The calculators give estimates based on published rules and the figures you enter. They are not tax, legal, financial or religious advice. Rules change, and your own situation may include details a calculator cannot account for.</p>
<ul>
<li><strong>Tax:</strong> your actual tax depends on your full income, exemptions and FBR's rules. Confirm with your employer, FBR or a tax adviser.</li>
<li><strong>Electricity:</strong> your actual bill includes monthly adjustments and other charges set by NEPRA and your distribution company.</li>
<li><strong>Job eligibility:</strong> the wording of each advertisement and the decision of the recruiting commission are final.</li>
<li><strong>Zakat:</strong> for questions about your own circumstances, consult a scholar.</li>
<li><strong>Grades:</strong> your board's or university's result is final.</li>
</ul>
<h2>Use of the site</h2>
<p>The site is free to use. We work to keep it accurate and available but cannot guarantee that it is error-free or always online, and we are not liable for decisions made using its results.</p>
<h2>Contact</h2>
<p>Report mistakes to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
""",
    },
]

// Run: node scripts/test.js  — checks every calculator against hand-worked figures.
const assert = require("assert");
const T = require("../assets/tools/salary-tax.js");
const A = require("../assets/tools/age-core.js");
const G = require("../assets/tools/govt-age.js");
const E = require("../assets/tools/electricity.js");
const Z = require("../assets/tools/zakat.js");
const P = require("../assets/tools/percentage.js");
const C = require("../assets/tools/cgpa.js");
const H = require("../assets/common.js");

let n = 0;
function eq(a, b, msg, tol = 0.01) { n++; assert.ok(Math.abs(a - b) <= tol, `${msg}: got ${a}, expected ${b}`); }
function is(a, b, msg) { n++; assert.deepStrictEqual(a, b, msg); }

// --- Salary tax, tax year 2027 (slab fixed amounts must chain) ---
const s = T.SLABS[2027];
for (let i = 1; i < s.length - 1; i++) eq(s[i][2] + (s[i][1] - s[i][0]) * s[i][3], s[i + 1][2], `2027 slab ${i} chains`);
const s6 = T.SLABS[2026];
for (let i = 1; i < s6.length - 1; i++) eq(s6[i][2] + (s6[i][1] - s6[i][0]) * s6[i][3], s6[i + 1][2], `2026 slab ${i} chains`);
eq(T.annualTax(600000, 2027).total, 0, "600k no tax");
eq(T.annualTax(1200000, 2027).total, 6000, "1.2M");
eq(T.annualTax(1800000, 2027).total, 72000, "1.8M");
eq(T.annualTax(3000000, 2027).total, 276000, "3.0M");
eq(T.annualTax(3000000, 2026).total, 300000, "3.0M last year");
eq(T.annualTax(6000000, 2027).total, 1104000, "6.0M");
eq(T.annualTax(6000000, 2026).total, 1281000, "6.0M last year");
eq(T.annualTax(12000000, 2027).total, 3174000, "12M");
eq(T.annualTax(12000000, 2026).total, 3381000 * 1.09, "12M last year with surcharge");
eq(T.calc(250000, "month").monthlyTax, 23000, "250k/month");
eq(T.calc(250000, "month").saving / 12, 2000, "250k saving");

// --- Age ---
const d = (s) => A.parse(s);
is(A.diff(d("1970-08-15"), d("1998-02-07"), true), { y: 27, m: 5, d: 24, days: 10039 }, "PPSC worked example");
is(A.diff(d("2000-01-31"), d("2000-03-01"), false).m, 1, "month borrow");
is(A.diff(d("2000-02-29"), d("2001-02-28"), false).y, 0, "leap day not yet a year");
is(A.diff(d("2000-02-29"), d("2001-03-01"), false).y, 1, "leap day after");
is(A.text({ y: 1, m: 0, d: 2 }), "1 year, 0 months, 2 days", "text");
is(A.parse("2026-02-30"), null, "invalid date");

// --- Govt age (FPSC) ---
let r = G.check({ dob: "1996-03-10", closing: "2026-11-20", minAge: 18, maxAge: 25, commission: "fpsc", category: "none", general: true });
is(r.age.y, 30, "age 30"); is(r.allowed, 30, "25+5"); is(r.eligible, true, "30 within 30");
is(A.iso(r.lastClosing), "2027-03-09", "eligible until the day before 31st birthday");
is(A.iso(r.earliestDob), "1995-11-21", "oldest DOB");
r = G.check({ dob: "1996-03-10", closing: "2027-03-10", minAge: 18, maxAge: 25, commission: "fpsc", category: "none", general: true });
is(r.eligible, false, "turns 31 on closing day");
r = G.check({ dob: "1980-01-01", closing: "2026-11-01", maxAge: 45, commission: "fpsc", category: "govt", general: true });
is(r.allowed, 55, "govt servant capped at 55");
r = G.check({ dob: "1990-01-01", closing: "2026-11-01", maxAge: 25, commission: "fpsc", category: "armed", served: 6, general: true });
is(r.allowed, 36, "armed: years served");
r = G.check({ dob: "1995-06-01", closing: "2026-11-01", maxAge: 25, commission: "ppsc", general: true, gender: "f", inclusive: true });
is(r.allowed, 33, "PPSC women 8 years");
r = G.check({ dob: "2010-01-01", closing: "2026-11-01", minAge: 18, maxAge: 25, commission: "other", custom: 0 });
is(r.underOk, false, "under age"); is(A.iso(r.firstClosing), "2028-01-01", "reaches 18");

// --- Electricity ---
let b = E.bill({ units: 150, type: "protected", load: 1, duty: false });
eq(b.energy, 1704.5, "protected 150 telescopic");
eq(b.fixed, 300, "protected fixed");
b = E.bill({ units: 150, type: "non", load: 1 });
eq(b.energy, 4336.5, "non-protected 150 single slab");
b = E.bill({ units: 201, type: "protected", load: 1 });
is(b.type, "non", "201 loses protection"); eq(b.energy, 6653.1, "201 units");
b = E.bill({ units: 300, type: "non", load: 2, duty: true, fpa: 0 });
eq(b.energy, 9930, "300 x 33.10"); eq(b.fixed, 700, "2kW x 350"); eq(b.fc, 969, "FC");
eq(b.ed, 148.95, "ED"); eq(b.gst, (9930 + 700 + 969 + 148.95) * 0.18, "GST");
b = E.bill({ units: 75, type: "lifeline", load: 1 });
eq(b.energy, 580.5, "lifeline 75"); eq(b.fixed, 0, "lifeline no fixed");
const cl = E.cliff({ units: 205, type: "protected", load: 1, duty: true });
assert.ok(cl && cl.edge === 200 && cl.saving > 4000, "cliff at 200"); n++;
is(E.cliff({ units: 250, type: "non", load: 1 }), null, "no cliff mid-slab");

// --- Zakat ---
let z = Z.calc({ cash: 600000, silverPrice: 9591, basis: "silver" });
eq(z.nisab, 503527.5, "silver nisab"); is(z.due, true, "due"); eq(z.zakat, 15000, "2.5% of 600k");
z = Z.calc({ cash: 400000, silverPrice: 9591 });
is(z.due, false, "below nisab");
z = Z.calc({ gold: 11.6638, unit: "g", goldPrice: 400000, cash: 0, silverPrice: 9591 });
eq(z.goldValue, 400000, "grams to tola");
z = Z.calc({ cash: 1000000, debts: 200000, goldPrice: 400000, basis: "gold" });
eq(z.nisab, 3000000, "gold nisab"); is(z.due, false, "below gold nisab");

// --- Percentage ---
let m = P.marks(1020, 1200);
eq(m.pct, 85, "85%"); is(m.newGrade[1], "A", "85 is A"); is(m.oldGrade[1], "A+", "old A+");
m = P.marks(1139, 1200); is(m.newGrade[1], "A+", "94.9% is A+ not A++");
m = P.marks(450, 1200); is(m.passNew, false, "37.5% fails new"); is(m.passOld, true, "passes old");
is(P.marks(1300, 1200), null, "over total");
is(P.needed(90, 1200, 1050), 30, "marks to A+");

// --- CGPA ---
const g = C.gpa([{ credits: 3, points: 4 }, { credits: 3, points: 3.33 }, { credits: 2, points: 3 }]);
eq(g.gpa, (12 + 9.99 + 6) / 8, "gpa"); is(C.show(2.996), "2.99", "truncate");
eq(C.cgpa(3.2, 60, 3.6, 18), (192 + 64.8) / 78, "cgpa");

// --- Formatting ---
is(H.money(1234567.4), "Rs 1,234,567", "money"); is(H.lakh(1250000), "12.5 lakh", "lakh"); is(H.lakh(23000000), "2.3 crore", "crore");

console.log(`All ${n} checks passed.`);

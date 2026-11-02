/* Salary income tax, Pakistan. Tax year 2027 (1 July 2026 – 30 June 2027) vs tax year 2026. */
(function (root) {
  "use strict";

  // [from, to, fixed tax at `from`, rate on the amount above `from`]
  var SLABS = {
    2027: [
      [0, 600000, 0, 0],
      [600000, 1200000, 0, 0.01],
      [1200000, 2200000, 6000, 0.11],
      [2200000, 3200000, 116000, 0.20],
      [3200000, 4100000, 316000, 0.25],
      [4100000, 5600000, 541000, 0.29],
      [5600000, 7000000, 976000, 0.32],
      [7000000, Infinity, 1424000, 0.35]
    ],
    2026: [
      [0, 600000, 0, 0],
      [600000, 1200000, 0, 0.01],
      [1200000, 2200000, 6000, 0.11],
      [2200000, 3200000, 116000, 0.23],
      [3200000, 4100000, 346000, 0.30],
      [4100000, Infinity, 616000, 0.35]
    ]
  };
  // Tax year 2026 had a 9% surcharge on tax for salaried income above Rs 10 million. Abolished for 2027.
  var SURCHARGE = { 2026: { above: 10000000, rate: 0.09 }, 2027: null };

  function slabFor(income, year) {
    var s = SLABS[year];
    for (var i = s.length - 1; i >= 0; i--) if (income > s[i][0]) return s[i];
    return s[0];
  }

  function annualTax(income, year) {
    if (!(income > 0)) return { base: 0, surcharge: 0, total: 0, slab: SLABS[year][0] };
    var sl = slabFor(income, year);
    var base = sl[2] + (income - sl[0]) * sl[3];
    var sc = SURCHARGE[year];
    var surcharge = sc && income > sc.above ? base * sc.rate : 0;
    return { base: base, surcharge: surcharge, total: base + surcharge, slab: sl };
  }

  function calc(amount, period) {
    var annual = period === "year" ? amount : amount * 12;
    var now = annualTax(annual, 2027);
    var before = annualTax(annual, 2026);
    return {
      annualIncome: annual,
      monthlyIncome: annual / 12,
      annualTax: now.total,
      monthlyTax: now.total / 12,
      slab: now.slab,
      effectiveRate: annual > 0 ? now.total / annual : 0,
      lastYearTax: before.total,
      saving: before.total - now.total,
      takeHomeMonthly: (annual - now.total) / 12
    };
  }

  var api = { SLABS: SLABS, annualTax: annualTax, calc: calc };

  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }
  root.SalaryTax = api;

  function pct(r) { return (Math.round(r * 1000) / 10).toString().replace(/\.0$/, "") + "%"; }

  function slabText(sl) {
    if (sl[3] === 0) return "Up to Rs 6 lakh, no tax";
    var to = sl[1] === Infinity ? "above Rs " + HPK.lakh(sl[0]) : "Rs " + HPK.lakh(sl[0]).replace(" lakh", "") + " to " + HPK.lakh(sl[1]);
    return pct(sl[3]) + ", " + to;
  }

  function run() {
    var out = HPK.$("result");
    var amount = HPK.num("salary");
    var period = HPK.radio("period") || "month";
    if (!(amount > 0)) {
      HPK.slip(out, { title: "Your tax for 2026-27", empty: "Enter your salary to see the tax deducted each month." });
      return;
    }
    var r = calc(amount, period);
    var lines = [
      { k: "Monthly salary", v: HPK.money(r.monthlyIncome) },
      { k: "Annual salary", v: HPK.money(r.annualIncome) },
      { k: "Your slab", v: slabText(r.slab) },
      { k: "Tax per year", v: HPK.money(r.annualTax) },
      { k: "Effective tax rate", v: pct(r.effectiveRate) },
      { k: "Take-home per month", v: HPK.money(r.takeHomeMonthly) }
    ];
    if (r.saving > 0.5) lines.push({ k: "You save vs 2025-26", v: HPK.money(r.saving / 12) + " a month", cls: "minus" });
    if (out.hasAttribute("data-compact")) lines = [lines[2], lines[3], lines[5]].concat(r.saving > 0.5 ? [lines[6]] : []);
    HPK.slip(out, {
      title: "Your tax for 2026-27",
      lines: lines,
      total: {
        k: "Tax deducted each month",
        v: HPK.money(r.monthlyTax),
        note: r.annualTax === 0 ? "Your salary is below the taxable limit of Rs 50,000 a month." :
          "Last year (2025-26) this salary paid " + HPK.money(r.lastYearTax / 12) + " a month."
      },
      foot: out.hasAttribute("data-compact") ? null : "Estimate on taxable salary under the Finance Act 2026. Your employer's figure can differ slightly because of allowances, exemptions or mid-year joining."
    });
  }

  document.addEventListener("DOMContentLoaded", function () { HPK.live("calc-form", run); });
})(this);

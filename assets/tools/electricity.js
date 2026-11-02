/* Domestic electricity bill estimate, Pakistan. Uniform tariff S.R.O. 279(I)/2026 (effective February 2026). */
(function (root) {
  "use strict";

  var NON_PROTECTED = [ // [up to units, Rs per unit, fixed Rs per kW]
    [100, 22.44, 275], [200, 28.91, 300], [300, 33.10, 350], [400, 36.46, 400],
    [500, 38.95, 500], [600, 40.22, 675], [700, 41.85, 675], [Infinity, 47.20, 675]
  ];
  var PROTECTED = [[100, 10.54, 200], [200, 13.01, 300]];
  var LIFELINE = [[50, 3.95, 0], [100, 7.74, 0]];
  var FC = { normal: 3.23, protectedRate: 1.43 };
  var GST = 0.18, ED = 0.015, TV_FEE = 35, WHT = { rate: 0.075, above: 25000 };

  function slabOf(table, units) {
    for (var i = 0; i < table.length; i++) if (units <= table[i][0]) return table[i];
    return table[table.length - 1];
  }

  function bill(o) {
    var units = Math.max(0, Math.round(o.units || 0));
    var kw = Math.max(1, Math.ceil(o.load || 1));
    var type = o.type || "non";
    var notes = [];
    if (type === "lifeline" && units > 100) { type = "protected"; notes.push("lifeline"); }
    if (type === "protected" && units > 200) { type = "non"; notes.push("protected"); }

    var energy, fixedRate, rateText, fcRate;
    if (type === "lifeline") {
      var s = slabOf(LIFELINE, units);
      energy = units * s[1]; fixedRate = 0; rateText = units + " × Rs " + s[1].toFixed(2); fcRate = FC.protectedRate;
    } else if (type === "protected") {
      var a = Math.min(units, 100), b = Math.max(0, units - 100);
      energy = a * PROTECTED[0][1] + b * PROTECTED[1][1];
      fixedRate = units <= 100 ? PROTECTED[0][2] : PROTECTED[1][2];
      rateText = b > 0 ? "100 × Rs 10.54 + " + b + " × Rs 13.01" : units + " × Rs 10.54";
      fcRate = FC.protectedRate;
    } else {
      var n = slabOf(NON_PROTECTED, units);
      energy = units * n[1]; fixedRate = n[2]; rateText = units + " × Rs " + n[1].toFixed(2); fcRate = FC.normal;
    }
    var fixed = units > 0 ? fixedRate * kw : 0;
    var fpa = units * (o.fpa || 0);
    var fc = units * fcRate;
    var ed = o.duty ? (energy + fpa) * ED : 0;
    var gst = (energy + fixed + fpa + fc + ed) * GST;
    var tv = o.tv ? TV_FEE : 0;
    var subtotal = energy + fixed + fpa + fc + ed + gst + tv;
    var wht = o.nonFiler && subtotal > WHT.above ? subtotal * WHT.rate : 0;
    return {
      units: units, kw: kw, type: type, notes: notes, rateText: rateText,
      energy: energy, fixed: fixed, fixedRate: fixedRate, fpa: fpa, fc: fc, fcRate: fcRate,
      ed: ed, gst: gst, tv: tv, wht: wht, total: subtotal + wht
    };
  }

  // If the units sit just above a slab line, how much would dropping to the line save?
  function cliff(o) {
    var r = bill(o);
    if (r.type !== "non" || r.units <= 100) return null;
    var edge = null;
    for (var i = 0; i < NON_PROTECTED.length - 1; i++) {
      var top = NON_PROTECTED[i][0];
      if (r.units > top && r.units - top <= 25) edge = top;
    }
    if (edge === null) return null;
    var lower = bill(Object.assign({}, o, { units: edge, type: o.type === "protected" && edge <= 200 ? "protected" : "non" }));
    return { edge: edge, fewer: r.units - edge, saving: r.total - lower.total };
  }

  var api = { bill: bill, cliff: cliff, NON_PROTECTED: NON_PROTECTED, PROTECTED: PROTECTED, LIFELINE: LIFELINE };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }
  root.ElectricityBill = api;

  function run() {
    var out = HPK.$("result");
    var o = {
      units: HPK.num("units"),
      type: HPK.radio("type") || "non",
      load: HPK.num("load") || 1,
      fpa: HPK.num("fpa") || 0,
      duty: HPK.$("duty").checked,
      tv: HPK.$("tv").checked,
      nonFiler: HPK.$("nonfiler").checked
    };
    var title = "Estimated bill";
    if (!(o.units > 0)) { HPK.slip(out, { title: title, empty: "Enter the units used this month. They are printed on your bill as \"Units consumed\"." }); return; }
    var r = bill(o);
    var names = { non: "Non-protected", protected: "Protected", lifeline: "Lifeline" };
    var lines = [
      { k: "Category used", v: names[r.type] },
      { k: "Energy charges", v: HPK.money(r.energy) },
      { k: r.rateText, v: "", cls: "sub" },
      { k: "Fixed charges (" + r.kw + " kW × Rs " + r.fixedRate + ")", v: HPK.money(r.fixed) },
      { k: "FC surcharge (Rs " + r.fcRate + "/unit)", v: HPK.money(r.fc) }
    ];
    if (r.fpa) lines.push({ k: "Fuel adjustment", v: HPK.money(r.fpa), cls: r.fpa < 0 ? "minus" : "" });
    if (r.ed) lines.push({ k: "Electricity duty (1.5%)", v: HPK.money(r.ed) });
    lines.push({ k: "GST (18%)", v: HPK.money(r.gst) });
    if (r.tv) lines.push({ k: "PTV fee", v: HPK.money(r.tv) });
    if (r.wht) lines.push({ k: "Income tax (7.5%, non-filer)", v: HPK.money(r.wht) });

    var alerts = [];
    if (r.notes.indexOf("protected") >= 0) alerts.push("More than 200 units means this bill is charged at non-protected rates, and you lose protected status for the next 6 months.");
    if (r.notes.indexOf("lifeline") >= 0) alerts.push("Lifeline status only covers up to 100 units, so this estimate uses protected rates.");
    var c = cliff(o);
    if (c && c.saving > 50) alerts.push("Using " + c.fewer + " fewer " + (c.fewer === 1 ? "unit" : "units") + " (" + c.edge + " instead of " + r.units + ") would cut this bill by about " + HPK.money(c.saving) + ".");

    HPK.slip(out, {
      title: title + " for " + r.units + " units",
      lines: lines,
      total: { k: "Estimated total", v: HPK.money(r.total), note: "About Rs " + (r.total / r.units).toFixed(2) + " per unit, all-in." },
      alerts: alerts,
      foot: "Arrears, quarterly adjustments and any other line on your bill are not included."
    });
  }

  document.addEventListener("DOMContentLoaded", function () { HPK.live("calc-form", run); });
})(this);

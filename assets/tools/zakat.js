/* Zakat calculator. Nisab: 52.5 tola silver or 7.5 tola gold. Rate 2.5%. */
(function (root) {
  "use strict";
  var TOLA_G = 11.6638;
  var NISAB_TOLA = { silver: 52.5, gold: 7.5 };
  var RATE = 0.025;

  function toTola(w, unit) { return unit === "g" ? w / TOLA_G : w; }

  function calc(o) {
    var unit = o.unit || "tola";
    var goldTola = toTola(o.gold || 0, unit), silverTola = toTola(o.silver || 0, unit);
    var goldValue = goldTola * (o.goldPrice || 0);
    var silverValue = silverTola * (o.silverPrice || 0);
    var assets = goldValue + silverValue + (o.cash || 0) + (o.bank || 0) + (o.business || 0) + (o.receivable || 0) + (o.investments || 0);
    var net = assets - (o.debts || 0);
    var basis = o.basis || "silver";
    var price = basis === "gold" ? o.goldPrice : o.silverPrice;
    var nisab = price > 0 ? NISAB_TOLA[basis] * price : null;
    var due = nisab != null && net >= nisab && net > 0;
    return {
      goldValue: goldValue, silverValue: silverValue, assets: assets, net: net,
      basis: basis, nisab: nisab, due: due, zakat: due ? net * RATE : 0
    };
  }

  var api = { calc: calc, TOLA_G: TOLA_G, NISAB_TOLA: NISAB_TOLA };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }
  root.Zakat = api;

  function run() {
    var out = HPK.$("result");
    var o = {
      unit: HPK.radio("unit") || "tola",
      gold: HPK.num("gold"), goldPrice: HPK.num("gold-price"),
      silver: HPK.num("silver"), silverPrice: HPK.num("silver-price"),
      cash: HPK.num("cash"), bank: HPK.num("bank"), business: HPK.num("business"),
      receivable: HPK.num("receivable"), investments: HPK.num("investments"),
      debts: HPK.num("debts"), basis: HPK.radio("basis") || "silver"
    };
    Object.keys(o).forEach(function (k) { if (typeof o[k] === "number" && isNaN(o[k])) o[k] = 0; });
    HPK.$("gold-price-field").querySelector(".hint").hidden = !(o.gold > 0 && !(o.goldPrice > 0));
    var title = "Your zakat";
    var r = calc(o);
    if (r.assets <= 0) { HPK.slip(out, { title: title, empty: "Enter what you own: cash, bank balance, gold, silver or business stock." }); return; }
    if (r.nisab == null) {
      HPK.slip(out, { title: title, empty: "Enter today's " + r.basis + " price per tola to work out the nisab." });
      return;
    }
    var lines = [];
    if (r.goldValue) lines.push({ k: "Gold", v: HPK.money(r.goldValue) });
    if (r.silverValue) lines.push({ k: "Silver", v: HPK.money(r.silverValue) });
    if (o.cash) lines.push({ k: "Cash in hand", v: HPK.money(o.cash) });
    if (o.bank) lines.push({ k: "Bank balance", v: HPK.money(o.bank) });
    if (o.business) lines.push({ k: "Business stock", v: HPK.money(o.business) });
    if (o.receivable) lines.push({ k: "Money owed to you", v: HPK.money(o.receivable) });
    if (o.investments) lines.push({ k: "Shares and savings", v: HPK.money(o.investments) });
    if (o.debts) lines.push({ k: "Less debts due now", v: "-" + HPK.money(o.debts), cls: "minus" });
    lines.push({ k: "Zakatable wealth", v: HPK.money(r.net) });
    lines.push({ k: "Nisab (" + NISAB_TOLA[r.basis] + " tola " + r.basis + ")", v: HPK.money(r.nisab) });
    HPK.slip(out, {
      title: title,
      lines: lines,
      total: r.due
        ? { k: "Zakat due (2.5%)", v: HPK.money(r.zakat), note: "Zakat is due once this wealth has stayed above the nisab for a full lunar year." }
        : { k: "Zakat due", v: "Rs 0", note: "Your wealth is " + HPK.money(Math.max(0, r.nisab - r.net)) + " below the nisab, so zakat is not due." },
      foot: "For questions about your own situation, such as jewellery in daily use or long-term loans, ask a scholar you trust."
    });
  }

  document.addEventListener("DOMContentLoaded", function () { HPK.live("calc-form", run); });
})(this);

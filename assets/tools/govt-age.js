/* Government job age eligibility with FPSC / PPSC age relaxation. Needs AgeCore. */
(function (root) {
  "use strict";
  var A = typeof module !== "undefined" && module.exports ? require("./age-core.js") : root.AgeCore;

  // FPSC relaxation categories (Initial Appointment to Civil Posts (Relaxation of Upper Age Limit) Rules, 1993).
  // Only one category applies; the 5-year general relaxation is added on top.
  var FPSC_CATS = {
    none: { label: "None", years: 0 },
    area: { label: "AJK, Gilgit-Baltistan, tribal areas, Scheduled Caste or Buddhist", years: 3 },
    govt: { label: "Government servant (2+ years continuous service)", years: 10, cap: 55 },
    armed: { label: "Retired or released armed forces", years: 15 },
    deceased: { label: "Widow, son or daughter of a federal employee who died in service", years: 5 }
  };

  function relaxation(o) {
    var parts = [], cap = null;
    if (o.commission === "fpsc") {
      var c = FPSC_CATS[o.category] || FPSC_CATS.none;
      var yrs = c.years;
      if (o.category === "armed") yrs = Math.min(15, Math.max(0, Math.floor(o.served || 0)));
      if (yrs > 0) parts.push({ k: c.label, years: yrs });
      if (c.cap) cap = c.cap;
      if (o.general) parts.push({ k: "General relaxation", years: 5 });
    } else if (o.commission === "ppsc") {
      if (o.general) parts.push({ k: "General relaxation (" + (o.gender === "f" ? "women" : "men") + ")", years: o.gender === "f" ? 8 : 5 });
      if (o.punjabService > 0) parts.push({ k: "Punjab government service", years: o.punjabService });
    } else if (o.custom > 0) {
      parts.push({ k: "Relaxation in the advert", years: o.custom });
    }
    var total = parts.reduce(function (s, p) { return s + p.years; }, 0);
    return { parts: parts, total: total, cap: cap };
  }

  function ageOn(dob, date, inclusive) { return A.diff(dob, date, inclusive); }

  // Search a few days around a guess for the boundary where test() flips.
  function boundary(guess, test, wantLast) {
    var d = A.addDays(guess, wantLast ? 4 : -4);
    var step = wantLast ? -1 : 1;
    for (var i = 0; i < 12; i++) {
      if (test(d)) return d;
      d = A.addDays(d, step);
    }
    return null;
  }

  function check(o) {
    var dob = A.parse(o.dob), close = A.parse(o.closing);
    if (!dob || !close) return { error: "dates" };
    if (dob.t >= close.t) return { error: "order" };
    var inc = !!o.inclusive;
    var age = ageOn(dob, close, inc);
    var rel = relaxation(o);
    var hasMax = o.maxAge > 0;
    var allowed = hasMax ? o.maxAge + rel.total : null;
    if (hasMax && rel.cap) allowed = Math.min(allowed, rel.cap);
    var hasMin = o.minAge > 0;

    var overOk = !hasMax || age.y <= allowed;
    var underOk = !hasMin || age.y >= o.minAge;

    var res = { age: age, rel: rel, allowed: allowed, overOk: overOk, underOk: underOk, eligible: overOk && underOk };

    if (hasMax) {
      // Earliest date of birth that is still within the upper limit on this closing date.
      res.earliestDob = boundary(A.addYears(close, -(allowed + 1)), function (d) { return ageOn(d, close, inc).y <= allowed; }, false);
      // Last closing date on which this person is still within the upper limit.
      res.lastClosing = boundary(A.addYears(dob, allowed + 1), function (d) { return ageOn(dob, d, inc).y <= allowed; }, true);
    }
    if (hasMin) {
      res.latestDob = boundary(A.addYears(close, -o.minAge), function (d) { return ageOn(d, close, inc).y >= o.minAge; }, true);
      res.firstClosing = boundary(A.addYears(dob, o.minAge), function (d) { return ageOn(dob, d, inc).y >= o.minAge; }, false);
    }
    return res;
  }

  var api = { check: check, relaxation: relaxation, FPSC_CATS: FPSC_CATS };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }
  root.GovtAge = api;

  function show(id, on) { var el = HPK.$(id); if (el) el.hidden = !on; }

  function run() {
    var out = HPK.$("result");
    var commission = HPK.radio("commission") || "fpsc";
    var cat = HPK.$("category").value;
    show("fpsc-opts", commission === "fpsc");
    show("ppsc-opts", commission === "ppsc");
    show("other-opts", commission === "other");
    show("served-field", commission === "fpsc" && cat === "armed");

    var o = {
      dob: HPK.$("dob").value,
      closing: HPK.$("closing").value,
      minAge: HPK.num("min-age") || 0,
      maxAge: HPK.num("max-age") || 0,
      commission: commission,
      category: cat,
      served: HPK.num("served") || 0,
      general: commission === "fpsc" ? HPK.$("general").checked : HPK.$("general-p").checked,
      gender: HPK.radio("gender") || "m",
      punjabService: HPK.num("pb-service") || 0,
      custom: HPK.num("custom-relax") || 0,
      inclusive: HPK.$("inclusive").checked
    };
    var title = "Age on the closing date";
    if (!o.dob || !o.closing) {
      HPK.slip(out, { title: title, empty: "Enter your date of birth and the advert's closing date." });
      return;
    }
    var r = check(o);
    if (r.error) {
      HPK.slip(out, { title: title, empty: r.error === "order" ? "The closing date must be after your date of birth." : "Check that both dates are valid." });
      return;
    }
    var lines = [];
    if (o.minAge > 0 || o.maxAge > 0) lines.push({ k: "Age limit in the advert", v: (o.minAge || "No minimum") + " to " + (o.maxAge || "no maximum") + (o.maxAge ? " years" : "") });
    r.rel.parts.forEach(function (p) { lines.push({ k: "+ " + p.k, v: p.years + (p.years === 1 ? " year" : " years"), cls: "sub" }); });
    if (r.allowed != null) lines.push({ k: "Your upper limit", v: r.allowed + " years" + (r.rel.cap && r.allowed === r.rel.cap ? " (capped)" : "") });
    if (r.earliestDob) lines.push({ k: "Oldest eligible birth date", v: A.pretty(r.earliestDob) });
    if (r.latestDob) lines.push({ k: "Youngest eligible birth date", v: A.pretty(r.latestDob) });

    var verdict = null, note;
    if (o.minAge > 0 || o.maxAge > 0) {
      if (r.eligible) {
        verdict = { ok: true, text: "You are within the age limit for this post." };
        note = r.lastClosing ? "You stay within this upper limit for adverts closing on or before " + A.pretty(r.lastClosing) + "." : null;
      } else if (!r.overOk) {
        verdict = { ok: false, text: "You are over the age limit by " + A.text(A.diff(r.lastClosing, A.parse(o.closing), false)).replace(/^0 years, /, "").replace(/^0 months, /, "") + "." };
        note = "Check whether another relaxation applies to you, such as government service.";
      } else {
        verdict = { ok: false, text: "You are under the minimum age for this post." };
        note = r.firstClosing ? "You reach the minimum age for adverts closing on or after " + A.pretty(r.firstClosing) + "." : null;
      }
    } else {
      note = "Add the age limit from the advert to check eligibility.";
    }
    HPK.slip(out, {
      title: title,
      lines: lines,
      total: { k: "Your age on " + A.pretty(A.parse(o.closing)), v: A.text(r.age), note: note },
      verdict: verdict,
      foot: "The advert's wording is final. Close to a limit? Check the exact dates in the advert."
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    HPK.live("calc-form", run);
    // PPSC adds one day when counting age; switch the default with the commission.
    document.querySelectorAll('input[name="commission"]').forEach(function (r) {
      r.addEventListener("change", function () { HPK.$("inclusive").checked = r.value === "ppsc"; run(); });
    });
  });
})(this);

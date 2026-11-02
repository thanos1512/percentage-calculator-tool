/* Exact age in years, months and days. Dates are "YYYY-MM-DD" strings, handled in UTC so time zones never shift a day. */
(function (root) {
  "use strict";

  function parse(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || "");
    if (!m) return null;
    var y = +m[1], mo = +m[2], d = +m[3];
    var t = Date.UTC(y, mo - 1, d);
    var chk = new Date(t);
    if (chk.getUTCMonth() !== mo - 1) return null;
    return { y: y, m: mo, d: d, t: t };
  }

  function fromTime(t) {
    var x = new Date(t);
    return { y: x.getUTCFullYear(), m: x.getUTCMonth() + 1, d: x.getUTCDate(), t: t };
  }

  function iso(o) {
    return o.y + "-" + String(o.m).padStart(2, "0") + "-" + String(o.d).padStart(2, "0");
  }

  function addDays(o, n) { return fromTime(o.t + n * 86400000); }

  function daysInMonth(y, m) { return new Date(Date.UTC(y, m, 0)).getUTCDate(); }

  // inclusive: count the end date as a full day (the PPSC method adds one day).
  function diff(from, to, inclusive) {
    if (inclusive) to = addDays(to, 1);
    var y = to.y - from.y, m = to.m - from.m, d = to.d - from.d;
    if (d < 0) {
      m -= 1;
      var pm = to.m - 1, py = to.y;
      if (pm === 0) { pm = 12; py -= 1; }
      d += daysInMonth(py, pm);
    }
    if (m < 0) { y -= 1; m += 12; }
    return { y: y, m: m, d: d, days: Math.round((to.t - from.t) / 86400000) };
  }

  // Same calendar day n years later (29 Feb falls back to 28 Feb).
  function addYears(o, n) {
    var y = o.y + n, d = Math.min(o.d, daysInMonth(y, o.m));
    return fromTime(Date.UTC(y, o.m - 1, d));
  }

  function text(a) {
    function p(n, w) { return n + " " + w + (n === 1 ? "" : "s"); }
    return p(a.y, "year") + ", " + p(a.m, "month") + ", " + p(a.d, "day");
  }

  function pretty(o) {
    var M = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return o.d + " " + M[o.m - 1] + " " + o.y;
  }

  function today() {
    var n = new Date();
    return fromTime(Date.UTC(n.getFullYear(), n.getMonth(), n.getDate()));
  }

  var api = { parse: parse, iso: iso, addDays: addDays, addYears: addYears, diff: diff, text: text, pretty: pretty, today: today, daysInMonth: daysInMonth };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.AgeCore = api;
})(this);

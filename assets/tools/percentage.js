/* Marks percentage with board grades, plus everyday percentage sums. */
(function (root) {
  "use strict";

  // IBCC grading for SSC / HSSC (pass mark 40%), being adopted by boards since 2023.
  var NEW_GRADES = [
    [95, "A++", "Exceptional"], [90, "A+", "Outstanding"], [85, "A", "Excellent"],
    [80, "B++", "Very good"], [75, "B+", "Good"], [70, "B", "Fairly good"],
    [60, "C", "Above average"], [50, "D", "Average"], [40, "E", "Below average"], [0, "U", "Unsatisfactory"]
  ];
  // Older grading still printed by some boards (pass mark 33%).
  var OLD_GRADES = [[80, "A+"], [70, "A"], [60, "B"], [50, "C"], [40, "D"], [33, "E"], [0, "F"]];

  function grade(p, table) {
    for (var i = 0; i < table.length; i++) if (p >= table[i][0]) return table[i];
    return table[table.length - 1];
  }

  function marks(obtained, total) {
    if (!(total > 0) || !(obtained >= 0) || obtained > total) return null;
    var p = obtained / total * 100;
    // Boards compare unrounded percentages against grade lines.
    return { pct: p, newGrade: grade(p, NEW_GRADES), oldGrade: grade(p, OLD_GRADES), passNew: p >= 40, passOld: p >= 33 };
  }

  function needed(target, total, obtained) { return Math.max(0, Math.ceil(target / 100 * total - obtained)); }

  var api = { marks: marks, grade: grade, NEW_GRADES: NEW_GRADES, OLD_GRADES: OLD_GRADES, needed: needed };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }
  root.Percentage = api;

  function fmt(n) { return (Math.round(n * 100) / 100).toString(); }

  function run() {
    var out = HPK.$("result");
    var ob = HPK.num("obtained"), tot = HPK.num("total");
    var title = "Your result";
    if (!(ob >= 0) || !(tot > 0)) { HPK.slip(out, { title: title, empty: "Enter your obtained marks and total marks." }); return; }
    var r = marks(ob, tot);
    if (!r) { HPK.slip(out, { title: title, empty: "Obtained marks can't be more than the total." }); return; }
    var lines = [
      { k: "Marks", v: HPK.group(ob, ob % 1 ? 2 : 0) + " out of " + HPK.group(tot) },
      { k: "Grade (new IBCC scale)", v: r.newGrade[1] + ", " + r.newGrade[2] },
      { k: "Grade (old scale)", v: r.oldGrade[1] }
    ];
    var next = null;
    for (var i = NEW_GRADES.length - 1; i >= 0; i--) if (NEW_GRADES[i][0] > r.pct) { next = NEW_GRADES[i]; break; }
    if (next) lines.push({ k: "Marks short of " + next[1], v: HPK.group(needed(next[0], tot, ob)) });
    HPK.slip(out, {
      title: title,
      lines: lines,
      total: { k: "Percentage", v: fmt(r.pct) + "%", note: r.passNew ? "Pass under the new 40% rule." : r.passOld ? "Below the new 40% pass mark, but above the old 33% mark." : "Below the pass mark." },
      foot: "Your board's result card is final. Some boards still use the old grades."
    });
  }

  function quick() {
    var a = HPK.num("q1a"), b = HPK.num("q1b");
    HPK.$("q1r").textContent = isFinite(a) && isFinite(b) ? fmt(a * b / 100) : "–";
    var c = HPK.num("q2a"), d = HPK.num("q2b");
    HPK.$("q2r").textContent = isFinite(c) && d ? fmt(c / d * 100) + "%" : "–";
    var e = HPK.num("q3a"), f = HPK.num("q3b");
    HPK.$("q3r").textContent = e && isFinite(f) ? (f >= e ? "+" : "") + fmt((f - e) / e * 100) + "%" : "–";
  }

  document.addEventListener("DOMContentLoaded", function () {
    HPK.live("calc-form", run);
    HPK.live("quick-form", quick);
  });
})(this);

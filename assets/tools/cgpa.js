/* Semester GPA and CGPA on the 4.00 scale used by most Pakistani universities. */
(function (root) {
  "use strict";
  var SCALE = [["A", 4.0], ["A-", 3.67], ["B+", 3.33], ["B", 3.0], ["B-", 2.67], ["C+", 2.33], ["C", 2.0], ["C-", 1.67], ["D+", 1.33], ["D", 1.0], ["F", 0]];

  function gpa(courses) {
    var cr = 0, pts = 0;
    courses.forEach(function (c) {
      if (c.credits > 0 && c.points >= 0) { cr += c.credits; pts += c.credits * c.points; }
    });
    return cr > 0 ? { gpa: pts / cr, credits: cr, points: pts } : null;
  }

  function cgpa(prevCgpa, prevCredits, semGpa, semCredits) {
    var c = (prevCredits || 0) + (semCredits || 0);
    if (!(c > 0)) return null;
    return ((prevCgpa || 0) * (prevCredits || 0) + semGpa * semCredits) / c;
  }

  // Floor to 2 decimals so a 2.996 is not shown as 3.00 (universities usually truncate).
  function show(x) { return (Math.floor(x * 100 + 1e-9) / 100).toFixed(2); }

  var api = { gpa: gpa, cgpa: cgpa, show: show, SCALE: SCALE };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }
  root.Cgpa = api;

  var n = 0;
  function addRow(credits, grade) {
    n++;
    var wrap = document.createElement("div");
    wrap.className = "course";
    var opts = SCALE.map(function (s) {
      return '<option value="' + s[1] + '"' + (s[0] === grade ? " selected" : "") + ">" + s[0] + " (" + s[1].toFixed(2) + ")</option>";
    }).join("");
    wrap.innerHTML =
      '<div class="cname"><label for="cn' + n + '">Course</label><input type="text" id="cn' + n + '" placeholder="Course ' + n + '"></div>' +
      '<div><label for="cr' + n + '">Credit hours</label><input type="number" inputmode="decimal" min="0" step="0.5" id="cr' + n + '" class="cr" value="' + (credits || 3) + '"></div>' +
      '<div><label for="gr' + n + '">Grade</label><select id="gr' + n + '" class="gr">' + opts + "</select></div>" +
      '<button type="button" class="ghost rm" aria-label="Remove course ' + n + '">Remove</button>';
    wrap.querySelector(".rm").addEventListener("click", function () {
      if (document.querySelectorAll(".course").length > 1) { wrap.remove(); run(); }
    });
    HPK.$("courses").appendChild(wrap);
  }

  function run() {
    var out = HPK.$("result");
    var courses = [];
    document.querySelectorAll(".course").forEach(function (row) {
      courses.push({ credits: Number(row.querySelector(".cr").value), points: Number(row.querySelector(".gr").value) });
    });
    var g = gpa(courses);
    var title = "Your GPA";
    if (!g) { HPK.slip(out, { title: title, empty: "Add credit hours for at least one course." }); return; }
    var prev = HPK.num("prev-cgpa"), prevCr = HPK.num("prev-credits");
    var lines = [
      { k: "Courses", v: String(courses.filter(function (c) { return c.credits > 0; }).length) },
      { k: "Credit hours", v: String(g.credits) },
      { k: "Quality points", v: (Math.round(g.points * 100) / 100).toString() }
    ];
    var total = { k: "Semester GPA", v: show(g.gpa) };
    if (prev >= 0 && prev <= 4 && prevCr > 0) {
      var c = cgpa(prev, prevCr, g.gpa, g.credits);
      lines.push({ k: "Semester GPA", v: show(g.gpa) });
      lines.push({ k: "Previous CGPA", v: show(prev) + " over " + prevCr + " credit hours" });
      total = { k: "New CGPA", v: show(c), note: "Over " + (prevCr + g.credits) + " credit hours in total." };
    }
    HPK.slip(out, { title: title, lines: lines, total: total, foot: "Uses the common 4.00 scale. If your university's grade points differ, pick the grade with the matching points." });
  }

  document.addEventListener("DOMContentLoaded", function () {
    [[3, "A"], [3, "B+"], [3, "A-"], [3, "B"], [2, "A"]].forEach(function (r) { addRow(r[0], r[1]); });
    HPK.$("add-course").addEventListener("click", function () { addRow(3, "B"); run(); });
    HPK.live("calc-form", run);
  });
})(this);

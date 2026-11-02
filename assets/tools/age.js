/* Exact age calculator. Needs AgeCore and HPK. */
(function () {
  "use strict";
  var A = window.AgeCore;
  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  function nextBirthday(dob, on) {
    var nb = A.addYears(dob, on.y - dob.y);
    if (nb.t < on.t) nb = A.addYears(dob, on.y - dob.y + 1);
    return nb;
  }

  function run() {
    var out = HPK.$("result");
    var dob = A.parse(HPK.$("dob").value);
    var on = A.parse(HPK.$("on").value) || A.today();
    var title = "Your age";
    if (!dob) { HPK.slip(out, { title: title, empty: "Enter your date of birth." }); return; }
    if (dob.t > on.t) { HPK.slip(out, { title: title, empty: "The date of birth is after the date you are checking." }); return; }
    var a = A.diff(dob, on, false);
    var nb = nextBirthday(dob, on);
    var toNext = A.diff(on, nb, false);
    var weeks = Math.floor(a.days / 7);
    HPK.slip(out, {
      title: title + " on " + A.pretty(on),
      lines: [
        { k: "Born on", v: DAYS[new Date(dob.t).getUTCDay()] + ", " + A.pretty(dob) },
        { k: "Total months", v: HPK.group(a.y * 12 + a.m) },
        { k: "Total weeks", v: HPK.group(weeks) + (a.days % 7 ? " and " + (a.days % 7) + " days" : "") },
        { k: "Total days", v: HPK.group(a.days) },
        { k: "Next birthday", v: A.pretty(nb) + " (" + DAYS[new Date(nb.t).getUTCDay()] + ")" },
        { k: "Days until it", v: toNext.days === 0 ? "Today. Happy birthday!" : HPK.group(toNext.days) }
      ],
      total: { k: "Exact age", v: A.text(a) }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var on = HPK.$("on");
    if (on && !on.value) on.value = A.iso(A.today());
    HPK.live("calc-form", run);
  });
})();

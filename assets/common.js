/* PakCalculators shared helpers. Works in the browser and in Node (for tests). */
(function (root) {
  "use strict";

  function round(n, d) {
    var f = Math.pow(10, d || 0);
    return Math.round((n + Number.EPSILON) * f) / f;
  }

  function group(n, decimals) {
    var neg = n < 0;
    var s = Math.abs(n).toFixed(decimals || 0);
    var parts = s.split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return (neg ? "-" : "") + parts.join(".");
  }

  function money(n, decimals) {
    if (!isFinite(n)) return "Rs 0";
    var d = decimals == null ? 0 : decimals;
    return (n < 0 ? "-Rs " : "Rs ") + group(Math.abs(round(n, d)), d);
  }

  // 1,250,000 -> "12.5 lakh"; 23,000,000 -> "2.3 crore"
  function lakh(n) {
    var a = Math.abs(n);
    if (a >= 1e7) return trim(a / 1e7) + " crore";
    if (a >= 1e5) return trim(a / 1e5) + " lakh";
    return group(a, 0);
  }
  function trim(x) { return String(round(x, 2)).replace(/\.0+$/, ""); }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  var api = { round: round, group: group, money: money, lakh: lakh, esc: esc };

  if (typeof document !== "undefined") {
    var ICON = {
      check: '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
      cross: '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 8v5"/><path d="M12 16.5v.01"/><circle cx="12" cy="12" r="9"/></svg>',
      pen: '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13.5 6.5l4 4"/></svg>',
      wa: '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.2-3.8A8 8 0 1 1 8 19z"/><path d="M9 8.8c0 3.3 2.9 6.2 6.2 6.2l1.3-1.6-2-1-1 .8a4 4 0 0 1-2.7-2.7l.8-1-1-2z"/></svg>',
      copy: '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5.5A1.5 1.5 0 0 0 14.5 4h-9A1.5 1.5 0 0 0 4 5.5v9A1.5 1.5 0 0 0 5.5 16H8"/></svg>'
    };
    var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // Count a number like "Rs 23,000", "85%" or "3.29" up from its previous value.
    var NUM = /^(-?)(Rs )?([\d,]+)(\.\d+)?(%?)$/;
    function parseShown(t) {
      var m = NUM.exec(t || "");
      if (!m) return null;
      var dec = m[4] ? m[4].length - 1 : 0;
      return { n: Number((m[1] || "") + m[3].replace(/,/g, "") + (m[4] || "")), rs: !!m[2], dec: dec, pct: m[5], comma: m[3].indexOf(",") >= 0 || Number(m[3].replace(/,/g, "")) >= 1000 };
    }
    function show(f, n) {
      var a = Math.abs(n).toFixed(f.dec);
      if (f.rs || f.comma) a = group(Math.abs(n), f.dec);
      return (n < 0 ? "-" : "") + (f.rs ? "Rs " : "") + a + f.pct;
    }
    function countUp(node, fromText) {
      var to = parseShown(node.textContent), from = parseShown(fromText);
      if (still || !to || !from || from.n === to.n) return;
      var start = null, dur = 450, a = from.n, b = to.n, finalText = node.textContent;
      function step(ts) {
        if (!node.isConnected) return;
        if (start === null) start = ts;
        var k = Math.min(1, (ts - start) / dur), e = 1 - Math.pow(1 - k, 3);
        node.textContent = k < 1 ? show(to, a + (b - a) * e) : finalText;
        if (k < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }

    var toastEl = null, toastTimer = null;
    function toast(msg) {
      if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
      toastEl.textContent = msg; toastEl.classList.add("show");
      clearTimeout(toastTimer); toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
    }
    api.toast = toast;

    api.$ = function (id) { return document.getElementById(id); };

    // Reads a number from an input; accepts "1,50,000" and "150000".
    api.num = function (id) {
      var el = document.getElementById(id);
      if (!el) return NaN;
      var v = String(el.value).replace(/[,\s]/g, "");
      return v === "" ? NaN : Number(v);
    };

    api.radio = function (name) {
      var el = document.querySelector('input[name="' + name + '"]:checked');
      return el ? el.value : null;
    };

    // Renders the bill-style result into a .slip element, and mirrors the total into the mobile result bar.
    api.slip = function (el, r) {
      var prevV = el.querySelector(".total .v");
      var prevText = prevV ? prevV.textContent : null;
      var h = '<p class="slip-title">' + esc(r.title) + '</p><div class="slip-body">';
      var bar = document.getElementById("result-bar");
      if (r.empty) {
        el.innerHTML = h + '<p class="empty">' + ICON.pen + "<span>" + esc(r.empty) + "</span></p></div>";
        if (bar) bar.hidden = true;
        return;
      }
      if (r.lines && r.lines.length) {
        h += '<ul class="lines">';
        r.lines.forEach(function (l) {
          h += '<li class="' + (l.cls || "") + '"><span class="k">' + esc(l.k) +
            '</span><span class="dots" aria-hidden="true"></span><span class="v">' + esc(l.v) + "</span></li>";
        });
        h += "</ul>";
      }
      if (r.total) {
        h += '<div class="total"><span class="k">' + esc(r.total.k) + '</span><span class="v">' +
          esc(r.total.v) + "</span>" + (r.total.note ? '<span class="note">' + esc(r.total.note) + "</span>" : "") + "</div>";
      }
      if (r.verdict) {
        h += '<div class="verdict ' + (r.verdict.ok ? "yes" : "no") + '">' + (r.verdict.ok ? ICON.check : ICON.cross) +
          "<span>" + esc(r.verdict.text) + "</span></div>";
      }
      (r.alerts || []).forEach(function (a) { h += '<p class="alert">' + esc(a) + "</p>"; });
      if (r.total && !el.hasAttribute("data-compact")) {
        h += '<div class="share"><button type="button" class="wa" data-share>' + ICON.wa + 'Share on WhatsApp</button>' +
          '<button type="button" class="ghost" data-copy>' + ICON.copy + "Copy result</button></div>";
      }
      if (r.foot) h += '<p class="slip-foot">' + esc(r.foot) + "</p>";
      el.innerHTML = h + "</div>";
      if (r.total) {
        el._shareText = r.total.k + ": " + r.total.v + (r.verdict ? "\n" + r.verdict.text : "") +
          "\nWorked out on PakCalculators: " + location.href.split("#")[0];
        var v = el.querySelector(".total .v");
        if (prevText === null) {
          var z = parseShown(r.total.v);
          if (z) countUp(v, show(z, 0));
        } else if (prevText !== r.total.v) {
          countUp(v, prevText);
          if (!still) v.parentNode.classList.add("bump");
        }
      }
      if (bar && r.total) {
        bar.querySelector(".rb-k").textContent = r.verdict ? r.verdict.text : r.total.k;
        bar.querySelector(".rb-v").textContent = r.total.v;
        bar.hidden = false;
      }
    };

    // Recalculate whenever any input inside the form changes.
    api.live = function (formId, fn) {
      var f = document.getElementById(formId);
      if (!f) return;
      f.addEventListener("input", fn);
      f.addEventListener("change", fn);
      f.addEventListener("submit", function (e) { e.preventDefault(); fn(); });
      fn();
    };

    // Show commas in rupee fields as the person types: 150000 -> 150,000.
    function formatMoney(input) {
      var raw = input.value;
      var caret = input.selectionStart == null ? raw.length : input.selectionStart;
      var digitsBefore = raw.slice(0, caret).replace(/[^\d.]/g, "").length;
      var clean = raw.replace(/[^\d.]/g, "");
      var dot = clean.indexOf(".");
      if (dot >= 0) clean = clean.slice(0, dot + 1) + clean.slice(dot + 1).replace(/\./g, "").slice(0, 2);
      var parts = clean.split(".");
      parts[0] = parts[0].replace(/^0+(?=\d)/, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      var out = parts.join(".");
      if (out === raw) return;
      input.value = out;
      var pos = 0, seen = 0;
      while (pos < out.length && seen < digitsBefore) { if (/[\d.]/.test(out[pos])) seen++; pos++; }
      try { input.setSelectionRange(pos, pos); } catch (e) {}
    }

    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll(".money input").forEach(function (inp) {
        formatMoney(inp);
        inp.addEventListener("input", function () { formatMoney(inp); });
      });

      // Mobile result bar: hide it while the full result is on screen.
      var bar = document.getElementById("result-bar"), slip = document.getElementById("result");
      if (bar && slip && "IntersectionObserver" in window) {
        document.body.classList.add("has-bar");
        new IntersectionObserver(function (es) {
          es.forEach(function (e) { bar.classList.toggle("off", e.isIntersecting); });
        }, { threshold: 0.25 }).observe(slip);
      }

      // Share and copy buttons in the result
      document.addEventListener("click", function (e) {
        var b = e.target.closest ? e.target.closest("[data-share],[data-copy]") : null;
        if (!b) return;
        var slipEl = b.closest(".slip"), text = slipEl && slipEl._shareText;
        if (!text) return;
        if (b.hasAttribute("data-share")) {
          window.open("https://wa.me/?text=" + encodeURIComponent(text), "_blank", "noopener");
        } else {
          var done = function () { toast("Result copied"); };
          if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () { toast("Couldn't copy. Select the result and copy it instead."); });
          else toast("Couldn't copy. Select the result and copy it instead.");
        }
      });

      // Quick example buttons fill the form
      document.querySelectorAll(".presets").forEach(function (row) {
        var btns = row.querySelectorAll("button");
        btns.forEach(function (btn) {
          btn.addEventListener("click", function () {
            var vals = JSON.parse(btn.getAttribute("data-fill"));
            Object.keys(vals).forEach(function (id) {
              var inp = document.getElementById(id);
              if (!inp) return;
              inp.value = vals[id];
              inp.dispatchEvent(new Event("input", { bubbles: true }));
            });
            btns.forEach(function (o) { o.setAttribute("aria-pressed", o === btn ? "true" : "false"); });
          });
        });
        var ids = [];
        btns.forEach(function (b) { Object.keys(JSON.parse(b.getAttribute("data-fill"))).forEach(function (k) { if (ids.indexOf(k) < 0) ids.push(k); }); });
        ids.forEach(function (id) {
          var inp = document.getElementById(id);
          if (inp) inp.addEventListener("input", function (e) { if (e.isTrusted) btns.forEach(function (o) { o.setAttribute("aria-pressed", "false"); }); });
        });
      });

      // Keep the current calculator's chip in view in the scrolling row.
      var chip = document.querySelector('.chip[aria-current="page"]');
      if (chip && chip.parentNode.scrollWidth > chip.parentNode.clientWidth) {
        chip.parentNode.scrollLeft = chip.offsetLeft - (chip.parentNode.clientWidth - chip.offsetWidth) / 2;
      }

      // Home page search
      var find = document.getElementById("tool-search");
      if (find) {
        var cards = [].slice.call(document.querySelectorAll("#tool-list > li"));
        var none = document.getElementById("no-match");
        find.addEventListener("input", function () {
          var q = find.value.trim().toLowerCase(), shown = 0;
          cards.forEach(function (c) {
            var hit = !q || c.getAttribute("data-find").indexOf(q) >= 0;
            c.hidden = !hit; if (hit) shown++;
          });
          none.hidden = shown > 0;
        });
      }

      // Theme toggle in the footer
      var btn = document.getElementById("theme-toggle");
      if (!btn) return;
      var rootEl = document.documentElement;
      function current() {
        var t = rootEl.getAttribute("data-theme");
        if (t) return t;
        return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
      }
      function label() { btn.textContent = current() === "dark" ? "Light mode" : "Dark mode"; }
      label();
      btn.addEventListener("click", function () {
        var next = current() === "dark" ? "light" : "dark";
        rootEl.setAttribute("data-theme", next);
        try { localStorage.setItem("hpk-theme", next); } catch (e) {}
        label();
      });
    });
  }

  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.HPK = api;
})(this);

/* HisaabPK shared helpers. Works in the browser and in Node (for tests). */
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

    // Renders the bill-style result into a .slip element.
    api.slip = function (el, r) {
      var h = '<p class="slip-title">' + esc(r.title) + "</p>";
      if (r.empty) {
        el.innerHTML = h + '<p class="empty">' + esc(r.empty) + "</p>";
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
        h += '<div class="verdict ' + (r.verdict.ok ? "yes" : "no") + '">' + esc(r.verdict.text) + "</div>";
      }
      (r.alerts || []).forEach(function (a) { h += '<p class="alert">' + esc(a) + "</p>"; });
      if (r.foot) h += '<p class="slip-foot">' + esc(r.foot) + "</p>";
      el.innerHTML = h;
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

    // Theme toggle in the footer
    document.addEventListener("DOMContentLoaded", function () {
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

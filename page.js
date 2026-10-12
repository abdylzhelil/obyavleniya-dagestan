/* Общие анимации страниц: появление блоков при прокрутке и плавные переходы между страницами.
   Без JavaScript и при «уменьшить движение» всё показывается сразу. */
(function () {
  var doc = document, root = doc.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 1. Появление блоков (.rv) на страницах ботов */
  function initReveal() {
    var items = doc.querySelectorAll(".rv");
    if (!items.length) return;
    if (reduce || !("IntersectionObserver" in window)) {
      items.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var counters = new Map();
    items.forEach(function (el) {
      var i = counters.get(el.parentElement) || 0;
      counters.set(el.parentElement, i + 1);
      el.style.setProperty("--d", Math.min(i, 6) * 70 + "ms");
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("in"); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    items.forEach(function (el) { io.observe(el); });
  }

  /* 2. Переходы между страницами.
     Современные браузеры делают их сами (@view-transition в CSS).
     Остальным — плавное затухание перед переходом и появление новой страницы. */
  var nativeTransitions = "CSSViewTransitionRule" in window;
  if (!nativeTransitions) root.classList.add("no-vt");

  function initLeave() {
    if (nativeTransitions || reduce) return;
    doc.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest && e.target.closest("a[href]");
      if (!a || a.target === "_blank" || a.hasAttribute("download")) return;
      var url;
      try { url = new URL(a.href, location.href); } catch (err) { return; }
      if (url.origin !== location.origin) return;
      if (url.pathname === location.pathname && url.search === location.search) return; /* якорь на этой же странице */
      e.preventDefault();
      root.classList.add("leaving");
      setTimeout(function () { location.href = url.href; }, 200);
    });
    window.addEventListener("pageshow", function (e) { if (e.persisted) root.classList.remove("leaving"); });
  }

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", initReveal); else initReveal();
  initLeave();
})();

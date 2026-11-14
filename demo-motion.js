/* Pause decorative demos offscreen or in hidden tabs.
   Respect reduced motion by default and allow an explicit per-demo opt-in. */
(function () {
  const reduce = typeof window.matchMedia === "function"
    ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  const demos = Array.from(document.querySelectorAll("[data-motion-demo]")).map(function (node) {
    return {
      node: node,
      button: document.querySelector('[data-motion-for="' + node.id + '"]'),
      visible: false,
      choice: null
    };
  });

  function enabled(demo) {
    return demo.choice === null ? !reduce.matches : demo.choice;
  }

  function update(demo) {
    const play = enabled(demo);
    demo.node.classList.toggle("demo-motion-enabled", reduce.matches && play);
    demo.node.classList.toggle("demo-motion-paused", !demo.visible || !play || document.hidden);
    if (!demo.button) return;
    const label = play ? "Приостановить анимацию"
      : (reduce.matches ? "Включить анимацию" : "Продолжить анимацию");
    demo.button.hidden = false;
    demo.button.setAttribute("aria-pressed", String(!play));
    demo.button.setAttribute("aria-label", label);
    demo.button.textContent = demo.button.hasAttribute("data-motion-compact")
      ? (play ? "Пауза" : (reduce.matches ? "Включить" : "Продолжить")) : label;
  }

  const observer = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      const demo = demos.find(function (item) { return item.node === entry.target; });
      if (!demo) return;
      demo.visible = entry.isIntersecting;
      update(demo);
    });
  }, { threshold: 0.1 }) : null;

  demos.forEach(function (demo) {
    if (demo.button) demo.button.addEventListener("click", function () {
      demo.choice = !enabled(demo);
      update(demo);
    });
    if (observer) observer.observe(demo.node);
    else demo.visible = true;
    update(demo);
  });

  document.addEventListener("visibilitychange", function () { demos.forEach(update); });
  function preferenceChanged() {
    demos.forEach(function (demo) { demo.choice = null; update(demo); });
  }
  if (reduce.addEventListener) reduce.addEventListener("change", preferenceChanged);
  else if (reduce.addListener) reduce.addListener(preferenceChanged);
})();

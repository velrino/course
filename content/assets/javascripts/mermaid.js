(function () {
  "use strict";

  function renderMermaid() {
    if (!window.mermaid) return;
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: "neutral",
    });
    const nodes = document.querySelectorAll(".mermaid:not([data-processed])");
    if (nodes.length) window.mermaid.run({ nodes }).catch(console.error);
  }

  if (typeof document$ !== "undefined") document$.subscribe(renderMermaid);
  else document.addEventListener("DOMContentLoaded", renderMermaid);
})();

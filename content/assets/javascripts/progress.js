(function () {
  "use strict";

  const STORAGE_KEY = "ai-automation-course-progress-v1";
  const FALLBACK_TOTAL = 154;

  function lessonId(pathname) {
    const decoded = decodeURIComponent(pathname);
    const match = decoded.match(
      /\/(\d{2}-[^/]+)\/(\d{2}-[^/]+?)(?:\.html|\/)?$/,
    );
    return match ? `${match[1]}/${match[2]}` : null;
  }

  function loadCompleted() {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      return new Set(Array.isArray(value) ? value.filter((item) => typeof item === "string") : []);
    } catch (_error) {
      return new Set();
    }
  }

  function saveCompleted(completed) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...completed].sort()));
    } catch (_error) {
      // Reading remains useful when storage is unavailable or full.
    }
  }

  function lessonsInNavigation() {
    const lessons = new Set();
    document.querySelectorAll(".md-nav__link[href]").forEach((link) => {
      const id = lessonId(new URL(link.href, window.location.href).pathname);
      if (id) lessons.add(id);
    });
    return lessons;
  }

  function renderProgress() {
    const article = document.querySelector("article.md-content__inner");
    if (!article) return;

    article.querySelector(".course-progress")?.remove();

    const knownLessons = lessonsInNavigation();
    const completed = loadCompleted();
    const currentLesson = lessonId(window.location.pathname);
    const total = knownLessons.size || FALLBACK_TOTAL;
    const completedCount = knownLessons.size
      ? [...completed].filter((id) => knownLessons.has(id)).length
      : Math.min(completed.size, total);

    const panel = document.createElement("section");
    panel.className = "course-progress";
    panel.setAttribute("aria-label", "Course progress");

    const header = document.createElement("div");
    header.className = "course-progress__header";
    header.innerHTML =
      '<span class="course-progress__label">Course progress</span>' +
      `<span aria-live="polite">${completedCount} of ${total} lessons complete</span>`;
    panel.append(header);

    const meter = document.createElement("progress");
    meter.max = total;
    meter.value = completedCount;
    meter.textContent = `${completedCount} of ${total}`;
    meter.setAttribute("aria-label", `${completedCount} of ${total} lessons complete`);
    panel.append(meter);

    if (currentLesson) {
      const button = document.createElement("button");
      const isComplete = completed.has(currentLesson);
      button.type = "button";
      button.className = "course-progress__button";
      button.setAttribute("aria-pressed", String(isComplete));
      button.textContent = isComplete ? "Mark lesson incomplete" : "Mark lesson complete";
      button.addEventListener("click", () => {
        if (completed.has(currentLesson)) completed.delete(currentLesson);
        else completed.add(currentLesson);
        saveCompleted(completed);
        renderProgress();
      });
      panel.append(button);
    }

    const heading = article.querySelector("h1");
    if (heading) heading.insertAdjacentElement("afterend", panel);
    else article.prepend(panel);
  }

  if (typeof document$ !== "undefined") document$.subscribe(renderProgress);
  else document.addEventListener("DOMContentLoaded", renderProgress);

  window.addEventListener("storage", (event) => {
    if (event.key === STORAGE_KEY) renderProgress();
  });
})();

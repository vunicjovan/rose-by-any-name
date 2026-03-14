const FALLBACK_COVER = "https://placehold.co/400x600?text=No+Cover";

// Persist theme preference
(function () {
  const saved = localStorage.getItem("rose-theme");
  const pref =
    saved ||
    (window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light");
  document.documentElement.setAttribute("data-theme", pref);
})();

async function loadBooks() {
  const res = await fetch("/api/books/");
  const books = await res.json();
  const grid = document.getElementById("book-grid");

  grid.innerHTML = books
    .map(
      (book) => `
    <div>
      <a href="/detail.html?id=${book.id}" class="book-card-link">
        <div class="uk-card uk-card-default uk-card-hover">
          <div class="uk-card-media-top cover-wrap">
            <img src="${book.cover_photo_url || FALLBACK_COVER}"
                 alt="Cover of ${book.title}"
                 onerror="this.src='${FALLBACK_COVER}'"
                 loading="lazy" />
          </div>
          <div class="uk-card-body">
            <p class="book-card-title">${book.title}</p>
            <p class="book-card-author">${book.author}</p>
            ${
              book.reading_year
                ? `<p class="book-card-year">
                   <span uk-icon="icon: calendar; ratio: 0.8"></span> Read in ${book.reading_year}
                 </p>`
                : ""
            }
          </div>
        </div>
      </a>
    </div>
  `,
    )
    .join("");
}

function initThemeToggle() {
  const btn = document.getElementById("theme-toggle");
  if (!btn) return;
  btn.addEventListener("click", function () {
    const next =
      document.documentElement.getAttribute("data-theme") === "dark"
        ? "light"
        : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("rose-theme", next);
  });
}

loadBooks();
initThemeToggle();

const FALLBACK_COVER = "https://placehold.co/400x600?text=No+Cover";

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

initThemeToggle();
loadBooks();

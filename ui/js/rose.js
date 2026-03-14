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
        <div class="uk-card uk-card-default uk-card-hover book-card">
          <div class="uk-card-media-top cover-wrap">
            <img src="${book.cover_photo_url || FALLBACK_COVER}"
                 alt="Cover of ${book.title}"
                 onerror="this.src='${FALLBACK_COVER}'"
                 loading="lazy" />
          </div>
          <div class="uk-card-body">
            <h3 class="uk-card-title uk-margin-remove-bottom">${book.title}</h3>
            <p class="uk-text-muted uk-margin-remove-top">${book.author}</p>
            ${
              book.reading_year
                ? `<p class="uk-text-small uk-margin-remove-top book-card-year">
                   <span uk-icon="icon: calendar; ratio: 0.85"></span> Read in ${book.reading_year}
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

loadBooks();

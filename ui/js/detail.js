const FALLBACK = "https://placehold.co/480x680?text=No+Cover";
const params = new URLSearchParams(location.search);
const bookId = params.get("id");

function show(id) {
  document.getElementById(id).hidden = false;
}
function hide(id) {
  document.getElementById(id).hidden = true;
}
function setText(id, text) {
  document.getElementById(id).textContent = text;
}

const META_FIELDS = [
  { icon: "calendar", label: "Print year", key: "print_year" },
  { icon: "bookmark", label: "Reading year", key: "reading_year" },
  { icon: "file-text", label: "Pages", key: "number_of_pages" },
  { icon: "world", label: "Original language", key: "original_language" },
  { icon: "comments", label: "Read in", key: "reading_language" },
];

function buildMetaTable(book) {
  const tbody = document.getElementById("meta-body");
  META_FIELDS.forEach(({ icon, label, key }) => {
    const value = book[key];
    if (value == null || value === "") return;
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td class="detail-meta-label">
        <span uk-icon="icon: ${icon}; ratio: 0.9"></span>
        ${label}
      </td>
      <td class="detail-meta-value">${value}</td>
    `;
    tbody.appendChild(tr);
  });
}

async function load() {
  if (!bookId) {
    hide("state-loading");
    setText("error-msg", "No book ID provided.");
    show("state-error");
    return;
  }

  let book;
  try {
    const res = await fetch(`/api/books/${bookId}`);
    if (!res.ok) throw new Error();
    book = await res.json();
  } catch {
    hide("state-loading");
    show("state-error");
    return;
  }

  document.title = `${book.title} — A Rose By Any Name`;
  setText("book-title", book.title);
  setText("book-author", book.author);

  const img = document.getElementById("cover-img");
  img.alt = `Cover of ${book.title}`;
  img.src = book.cover_photo_url || FALLBACK;
  img.onerror = () => {
    img.src = FALLBACK;
  };

  buildMetaTable(book);

  if (book.summary) {
    setText("book-summary", book.summary);
    show("summary-section");
  }

  if (book.user_rating > 0 || book.user_remarks) {
    show("reader-section");
  }
  if (book.user_rating > 0) {
    const pct = (book.user_rating / 10) * 100;
    document.getElementById("star-fill").style.width = `${pct}%`;
    document.getElementById("star-label").textContent =
      `${book.user_rating.toFixed(1)} / 10`;
    show("rating-section");
  }
  if (book.user_remarks) {
    setText("book-remarks-text", book.user_remarks);
    show("remarks-section");
  }

  document.getElementById("edit-btn").href = `/add.html?id=${book.id}`;
  document.getElementById("delete-btn").addEventListener("click", async () => {
    try {
      await UIkit.modal.confirm(
        `Delete "<strong>${book.title}</strong>"? This cannot be undone.`,
        { labels: { ok: "Delete", cancel: "Cancel" } },
      );
    } catch {
      return; // user cancelled
    }
    await fetch(`/api/books/${book.id}`, { method: "DELETE" });
    location.href = "/";
  });

  hide("state-loading");
  show("book-detail");
}

initThemeToggle();
load();

const params = new URLSearchParams(location.search);
const bookId = params.get("id");
const form = document.getElementById("book-form");

// Live cover preview
const coverInput = document.getElementById("cover_photo_url");
const previewWrap = document.getElementById("cover-preview-wrap");
const previewImg = document.getElementById("cover-preview");

coverInput.addEventListener("input", () => {
  const url = coverInput.value.trim();
  if (url) {
    previewImg.src = url;
    previewWrap.hidden = false;
  } else {
    previewWrap.hidden = true;
  }
});

function showError(msg) {
  const box = document.getElementById("form-error");
  document.getElementById("form-error-msg").textContent = msg;
  box.hidden = false;
}

function hideError() {
  document.getElementById("form-error").hidden = true;
}

function getFormData() {
  const intOrNull = (v) => (v !== "" ? parseInt(v, 10) : null);
  return {
    title: form.title.value.trim(),
    author: form.author.value.trim(),
    print_year: intOrNull(form.print_year.value),
    reading_year: intOrNull(form.reading_year.value),
    number_of_pages: intOrNull(form.number_of_pages.value),
    original_language: form.original_language.value.trim() || null,
    reading_language: form.reading_language.value.trim() || null,
    summary: form.summary.value.trim() || null,
    cover_photo_url: form.cover_photo_url.value.trim() || null,
    user_rating:
      form.user_rating.value !== "" ? parseFloat(form.user_rating.value) : 0,
    user_remarks: form.user_remarks.value.trim() || null,
  };
}

function fillForm(book) {
  form.title.value = book.title ?? "";
  form.author.value = book.author ?? "";
  form.print_year.value = book.print_year ?? "";
  form.reading_year.value = book.reading_year ?? "";
  form.number_of_pages.value = book.number_of_pages ?? "";
  form.original_language.value = book.original_language ?? "";
  form.reading_language.value = book.reading_language ?? "";
  form.summary.value = book.summary ?? "";
  form.cover_photo_url.value = book.cover_photo_url ?? "";
  form.user_rating.value = book.user_rating ?? "";
  form.user_remarks.value = book.user_remarks ?? "";
  if (book.cover_photo_url) {
    previewImg.src = book.cover_photo_url;
    previewWrap.hidden = false;
  }
}

async function init() {
  if (bookId) {
    document.getElementById("page-title").textContent = "Edit Book";
    document.getElementById("submit-btn").textContent = "Update Book";
    document.getElementById("back-btn").href = `/detail.html?id=${bookId}`;
    document.getElementById("cancel-btn").href = `/detail.html?id=${bookId}`;
    const res = await fetch(`/api/books/${bookId}`);
    if (!res.ok) {
      showError("Book not found.");
      return;
    }
    fillForm(await res.json());
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideError();

  const data = getFormData();
  if (!data.title) {
    showError("Title is required.");
    return;
  }
  if (!data.author) {
    showError("Author is required.");
    return;
  }

  const url = bookId ? `/api/books/${bookId}` : "/api/books/";
  const method = bookId ? "PUT" : "POST";

  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    showError(err.detail ?? "Something went wrong. Please try again.");
    return;
  }

  location.href = bookId ? `/detail.html?id=${bookId}` : "/";
});

initThemeToggle();
init();

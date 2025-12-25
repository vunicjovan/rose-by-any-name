from pathlib import Path

import gradio as gr

from src.repository.book_repository import BookRepository
from src.ui.book_grid import BookGrid


class RoseApp:
    def __init__(self):
        self.title = "🌹 A Rose By Any Name"
        self.books = BookRepository.get_books()

    def build(self) -> gr.Blocks:
        with gr.Blocks(title=self.title) as demo:
            gr.Markdown(f"## {self.title}")
            gr.HTML(BookGrid.render(self.books))
        return demo

    def launch(self):
        css_path = Path(__file__).parent / "static/styles/rose.css"
        self.build().launch(css_paths=str(css_path))


if __name__ == "__main__":
    RoseApp().launch()

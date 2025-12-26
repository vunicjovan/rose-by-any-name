from pathlib import Path

import gradio as gr

from src.services.book_service import BookService
from src.ui.book_form import BookForm
from src.ui.book_grid import BookGrid


class RoseApp:
    def __init__(self):
        self.title: str = "🌹 A Rose By Any Name"
        self.service: BookService = BookService()

    def build(self) -> gr.Blocks:
        with gr.Blocks(title=self.title) as demo:
            gr.Markdown(f"## {self.title}")

            with gr.Sidebar(open=False):
                gr.HTML(BookForm.render(action="/add"))

            gr.HTML(BookGrid.render(self.service.list()))

        return demo

    def launch(self):
        css_path = Path(__file__).parent / "static/styles/rose.css"
        self.build().launch(css_paths=str(css_path))


if __name__ == "__main__":
    RoseApp().launch()

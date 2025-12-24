import gradio as gr


def greet(name: str, intensity: float) -> str:
    return "Hello, " + name + "!" * int(intensity)


def main() -> None:
    demo = gr.Interface(
        fn=greet,
        inputs=["text", "slider"],
        outputs=["text"],
        api_name="predict",
    )

    demo.launch()


if __name__ == "__main__":
    main()

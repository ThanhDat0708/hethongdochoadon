import gradio as gr
import main as hethongdochoadon

HEADER_HTML = """
<div style="
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    margin-bottom: 1rem;
    color: white;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
">
    <h1 style="margin: 0; font-size: 1.8rem;">He Thong Doc Hoa Don</h1>
    <p style="margin: 0.5rem 0 0; opacity: 0.9; font-size: 1rem;">
        Nhap hoa don dang van ban hoac tai anh de phan tich tu dong
    </p>
</div>
"""


def process_invoice(message, history, image):
    if history is None:
        history = []

    if not message and not image:
        history.append({"role": "assistant", "content": "Vui lòng nhap hoa đơn hoặc tải ảnh hóa đơn."})
        return history, None, ""

    user_text = message if message else "Da gui anh hoa don"
    history.append({"role": "user", "content": user_text})

    try:
        invoice = hethongdochoadon.Information_Invoice(
            text=message if message else None,
            image=image
        )

        lines = ["Ket qua phan tich:\n"]
        for item in invoice.items:
            total = item.price * item.quantity
            lines.append(
                f"- **{item.name_food}**: {item.price:,.0f}₫ × {item.quantity} = **{total:,.0f}₫**"
            )

        tong = sum(item.price * item.quantity for item in invoice.items)
        lines.append(f"\n---\n**Tong cong: {tong:,.0f} VND**")

        history.append({"role": "assistant", "content": "\n".join(lines)})
    except Exception as e:
        history.append({"role": "assistant", "content": f"**Loi:** {str(e)}"})

    return history, None, ""


with gr.Blocks(
    title="He Thong Doc Hoa Don"
) as demo:
    gr.HTML(HEADER_HTML)

    chatbot = gr.Chatbot(
        height=420,
        avatar_images=(None, None),
        render_markdown=True,
    )

    with gr.Row():
        txt = gr.Textbox(
            label="Nhap hoa don",
            placeholder="VD: Pho bo 45000 x 2\nTra da 5000 x 3",
            lines=2,
            scale=4,
            container=True,
        )
        img = gr.Image(
            type="filepath",
            label="Tai anh",
            height=100,
            scale=1,
        )

    with gr.Row():
        send_btn = gr.Button("Gui", variant="primary", size="lg", scale=2)
        clear_btn = gr.Button("Xoa lich su", size="lg", scale=1)

    send_btn.click(
        fn=process_invoice,
        inputs=[txt, chatbot, img],
        outputs=[chatbot, img, txt],
    )

    txt.submit(
        fn=process_invoice,
        inputs=[txt, chatbot, img],
        outputs=[chatbot, img, txt],
    )

    clear_btn.click(
        fn=lambda: ([], None, ""),
        outputs=[chatbot, img, txt],
    )

if __name__ == "__main__":
    demo.launch(
        theme=gr.themes.Soft(primary_hue="purple"),
    )

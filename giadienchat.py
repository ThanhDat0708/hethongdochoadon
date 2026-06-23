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
    <h1 style="margin: 0; font-size: 1.8rem;">🧾 Hệ Thống Đọc Hóa Đơn</h1>
    <p style="margin: 0.5rem 0 0; opacity: 0.9; font-size: 1rem;">
        Nhập hóa đơn dạng văn bản hoặc tải ảnh để phân tích tự động
    </p>
</div>
"""


def process_invoice(message, history, image):
    if history is None:
        history = []

    if not message and not image:
        history.append((None, "⚠️ Vui lòng nhập hóa đơn hoặc tải ảnh hóa đơn."))
        return history, None, ""

    user_text = message if message else "📷 Đã gửi ảnh hóa đơn"
    history.append((user_text, None))

    try:
        invoice = hethongdochoadon.Information_Invoice(
            text=message if message else None,
            image=image
        )

        lines = ["**📋 Kết quả phân tích:**\n"]
        for item in invoice.items:
            total = item.price * item.quantity
            lines.append(
                f"- **{item.name_food}**: {item.price:,.0f}₫ × {item.quantity} = **{total:,.0f}₫**"
            )

        tong = sum(item.price * item.quantity for item in invoice.items)
        lines.append(f"\n---\n**💵 Tổng cộng: {tong:,.0f} VND**")

        history.append((None, "\n".join(lines)))
    except Exception as e:
        history.append((None, f"❌ **Lỗi:** {str(e)}"))

    return history, None, ""


with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="purple"),
    title="Hệ Thống Đọc Hóa Đơn"
) as demo:
    gr.HTML(HEADER_HTML)

    chatbot = gr.Chatbot(
        height=420,
        bubble_full_width=False,
        avatar_images=(None, "🧾"),
        render_markdown=True,
    )

    with gr.Row():
        txt = gr.Textbox(
            label="Nhập hóa đơn",
            placeholder="VD: Phở bò 45000 x 2\nTrà đá 5000 x 3",
            lines=2,
            scale=4,
            container=True,
        )
        img = gr.Image(
            type="filepath",
            label="Tải ảnh",
            height=100,
            scale=1,
        )

    with gr.Row():
        send_btn = gr.Button("📤 Gửi", variant="primary", size="lg", scale=2)
        clear_btn = gr.Button("🔄 Xóa lịch sử", size="lg", scale=1)

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
        fn=lambda: (None, None, ""),
        outputs=[chatbot, img, txt],
    )

if __name__ == "__main__":
    demo.launch()

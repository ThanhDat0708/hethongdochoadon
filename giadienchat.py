import gradio as gr
import main as hethongdochoadon

with gr.Blocks() as app:

    gr.Markdown("# Hệ Thống Đọc Hóa Đơn")

    txt_invoice = gr.Textbox(
        label="Nhập hóa đơn",
        lines=5
    )

    img_invoice = gr.Image(
        type="filepath",
        label="Tải ảnh hóa đơn"
    )

    output = gr.Textbox(
        label="Kết quả"
    )

    btn = gr.Button("Phân tích")

    btn.click(
        fn=hethongdochoadon.Information_Invoice,
        inputs=[txt_invoice, img_invoice],
        outputs=output
    )

app.launch()
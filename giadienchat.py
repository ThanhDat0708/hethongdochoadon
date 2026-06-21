import gradio as gr  
import main as hethongdochoadon

app = gr.ChatInterface(
    fn=hethongdochoadon.Information_Invoice,
    title='Hệ Thống Đọc Hóa Đơn'
)
app.launch()





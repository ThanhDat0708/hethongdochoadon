import gradio as gr  
import main as hethongdochoadon

app = gr.ChatInterface(
    fn=hethongdochoadon.Infornation_Invoice,
    title='Hệ Thống Đọc Hóa Đơn'
)
app.launch()





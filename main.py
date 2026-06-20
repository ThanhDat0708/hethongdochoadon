from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import base64

load_dotenv()
client = OpenAI()
class DataFoodItem(BaseModel):
    name_food: str
    price: float
    quantity: int

class Invoice(BaseModel):
    items: list[DataFoodItem]
def Infornation_Invoice(text, image):
    
    if image is not None:

        with open(image,"rb") as file_invoice:
            img_base64 = base64.b64encode(
                file_invoice.read()
            ).decode()
    chat_histories = []
    chat_histories.append(
        {
            'role':'user',
            'content':
            [
                {
                    'type':'input_text',
                    'text':'Hãy đọc hóa đơn'
                },
                {
                        'type':'input_image',
                        'image_url':f"data:image/jpeg;base64,{img_base64}"
                }
                
            ]

        }
    )
    response = client.responses.parse(
        instructions="""Bạn là một chuyên gia đọc hóa đơn món ăn
        Hãy trích xuất:
        -Tên món ăn
        -Giá món ăn
        -Số lượng
        Trả đúng schema JSON.""",
        model= 'gpt-5.4-mini',
        input=chat_histories, 
        temperature=0.1,
        text_format=Invoice
    )

invoice = Infornation_Invoice(text,image)

tong_hd = sum(
    item.price * item.quantity
    for item in invoice.items
)

print(f"Tổng tiền: {tong_hd}.VND")
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
client = OpenAI()
chat_histories = []

class DataFoodItem(BaseModel):
    name_food: str
    price: float
    quantity: int

class Invoice(BaseModel):
    items: list[DataFoodItem]

while True:
    user_input = input('Chat ở đây:')

    if not user_input:
        break
    
    chat_histories.append(
        {
            'role':'user',
            'content':user_input
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

invoice = response.output_parsed
print(invoice)

tong_hd = sum(
    item.price * item.quantity
    for item in invoice.items
)

print(f"Tổng tiền: {tong_hd}.VND")
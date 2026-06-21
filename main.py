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

def Information_Invoice(text=None, image=None):
    chat_histories = []
    # upload ảnh
    if image is not None:
        with open(image, "rb") as file_invoice:
            img_base64 = base64.b64encode(
                file_invoice.read()
            ).decode()
        chat_histories.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Hãy đọc hóa đơn này"
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{img_base64}"
                    }
                ]
            }
        )
    #  text
    elif text:
        chat_histories.append(
            {
                "role": "user",
                "content": text
            }
        )
    else:
        raise ValueError(
            "Vui lòng nhập hóa đơn hoặc tải ảnh hóa đơn."
        )
    response = client.responses.parse(
        instructions="""
        Bạn là một chuyên gia đọc hóa đơn món ăn.

        Hãy trích xuất:
        - Tên món ăn
        - Giá món ăn
        - Số lượng
        Trả đúng schema JSON.
        """,
        model="gpt-5.4-mini",
        input=chat_histories,
        temperature=0.1,
        text_format=Invoice
    )
    invoice = response.output_parsed

    tong_hd = sum(
        item.price * item.quantity
        for item in invoice.items
)
    print(f"Tổng tiền: {tong_hd:,.0f} VND")
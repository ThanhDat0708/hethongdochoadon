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
    content = []

    if image is not None:
        with open(image, "rb") as file_invoice:
            img_base64 = base64.b64encode(
                file_invoice.read()
            ).decode()
        content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{img_base64}"
        })

    if text:
        content.append({"type": "input_text", "text": text})
    elif image:
        content.append({"type": "input_text", "text": "Hãy đọc hóa đơn này"})
    else:
        raise ValueError("Vui lòng nhập hóa đơn hoặc tải ảnh hóa đơn.")

    chat_histories.append({"role": "user", "content": content})
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

    return response.output_parsed

if __name__ == "__main__":
    invoice = Information_Invoice(
        text="""
        Phở bò 45000 x 2
        Trà đá 5000 x 3
        """
    )

    print(invoice)

    tong_hd = sum(
        item.price * item.quantity
        for item in invoice.items
    )

    print(f"Tổng tiền: {tong_hd:,.0f} VND")
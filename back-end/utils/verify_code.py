# 验证码.py
import base64
import random
import string
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

class ImageCode():
    def __init__(self):
        self.width = 120
        self.height = 50

    def get_text(self):
        return "".join(random.sample(string.ascii_uppercase+string.digits,4))

    def draw_lines(self,draw,num,height,width):
        for i in range(num):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)

            draw.line(((x1,y1),(x2,y2)),fill="black",width=2)

    def get_code(self):
        code = self.get_text()
        print(code)
        img = Image.new('RGB', (self.width,self.height),"white")

        font = ImageFont.truetype("arial.ttf",35)
        draw = ImageDraw.Draw(img)
        # 把验证码画到图上
        for i in range(4):
            draw.text((random.randint(1,10)+30*i,random.randint(5,10)),
                      text=code[i],fill="black",font=font)
        self.draw_lines(draw,3,self.width,self.height)

        buf = BytesIO()
        img.save(buf, format='JPEG')
        # image_b_string = buf.getvalue()
        buf.seek(0)

        # 转换为base64字符串
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        # img.show()
        return code,image_base64

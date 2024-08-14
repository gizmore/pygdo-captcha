import random
from io import BytesIO

from PIL import Image, ImageFilter, ImageDraw, ImageFont

from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.base.Util import Random
from gdo.core.GDT_Char import GDT_Char
from gdo.core.GDT_Raw import GDT_Raw
from gdo.ui.GDT_Color import GDT_Color
from gdo.ui.GDT_Font import GDT_Font
from gdo.ui.GDT_Height import GDT_Height
from gdo.ui.GDT_Width import GDT_Width


class render(Method):

    def gdo_trigger(self) -> str:
        return ''

    def gdo_parameters(self) -> [GDT]:
        return [
            # GDT_Char('static').minlen(5),
            GDT_Width('width').initial('240').not_null(),
            GDT_Height('height').initial('64').not_null(),
            GDT_Color('bg').initial('#ffffff00').not_null(),
            GDT_Color('fg').initial('#999999ff').not_null(),
        ]

    def is_static(self) -> bool:
        return self.param_value('static') is not None

    def get_captcha_text(self):
        old = Application.get_session().get('captcha_solved')
        return old or ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5))

    def execute(self):
        width = self.param_value('width')
        height = self.param_value('height')
        bg = self.param_val('bg')
        fg = self.param_val('fg')

        captcha_text = self.get_captcha_text()

        if not self.is_static():
            Application.get_session().set('captcha', captcha_text)

        image = Image.new('RGB', (width, height), bg)
        font = self.get_font()

        # Draw each letter with random rotation and position
        for i, char in enumerate(captcha_text):
            # Create a separate image for each character to rotate it
            char_image = Image.new('RGBA', (50, 50), bg)
            char_draw = ImageDraw.Draw(char_image)
            char_draw.text((10, 5), char, font=font, fill=fg)

            # Rotate the character image
            angle = random.randint(-30, 30)
            rotated_char_image = char_image.rotate(angle, expand=1, fillcolor=bg)

            # Paste the rotated character onto the main image
            w5 = int((width - 10) / 5)
            x = 10 + i * w5 + random.randint(-15, 5)
            y = random.randint(-5, 5)
            image.paste(rotated_char_image, (x, y), rotated_char_image)

        # image = image.filter(ImageFilter.BLUR)
        draw = ImageDraw.Draw(image)

        # # Draw some random lines for additional noise
        for i in range(20):
            start = (random.randint(0, width), random.randint(0, height))
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([start, end], fill=fg, width=2)

        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

        # Save or display the image
        buffer = BytesIO()
        image.save(buffer, format='gif')
        buffer.seek(0)
        Application.header('Content-Type', 'image/gif')
        return GDT_Raw('result').val(buffer.read())
        # return image.show()  # Or use image.save("captcha.png") to save

    def get_font(self):
        fonts = GDT_Font.FONTS
        path = fonts[Random.list_item(list(fonts.keys()))]
        return ImageFont.truetype(path, 40)

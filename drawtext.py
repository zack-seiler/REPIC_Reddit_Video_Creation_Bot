from PIL import Image, ImageDraw, ImageFont
import textwrap
import os


def create_image(text_input, name, style):
    """
    Create an image with the given text, name, and style.

    param text_input: str, the text to display on the image
    param name: str, the name of the image file
    param style: int, a value between 1 and 3 indicating the desired style
    return: None, saves the image as a PNG file in the 'Data_Cache' directory
    """

    if style == 1:
        # Style 1: OpenSans-Regular font, light gray text on a semi-transparent dark gray background
        text_input = textwrap.fill(text_input, width=50)
        size = (1080, 600)
        bg_color = (38, 38, 38, 175)
        font_color = (196, 196, 196)
        ttf_file = os.path.join(os.getcwd(), "Font\\OpenSans-Regular.ttf")
        font = ImageFont.truetype(ttf_file, size=35)
        W, H = size
        image = Image.new('RGBA', size, bg_color)
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), text_input, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), text_input, font=font, fill=font_color, align="center",
                  stroke_width=2, stroke_fill="black")
        image.save(os.path.join(os.getcwd(), "Data_Cache\\" + name + ".png"))

    elif style == 2:
        # Style 2: Streetwear font, white text with black stroke on a transparent background
        text_input = textwrap.fill(text_input, width=25)
        size = (1080, 600)
        font_color = (255, 255, 255)
        ttf_file = os.path.join(os.getcwd(), "Font\\Streetwear.otf")
        font = ImageFont.truetype(ttf_file, size=100)
        W, H = size
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), text_input, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), text_input, font=font, fill=font_color, align="center", spacing=25,
                  stroke_width=5, stroke_fill="black")
        image.save(os.path.join(os.getcwd(), "Data_Cache\\Subreddit_Title.png"))

    elif style == 3:
        # Style 3: Coolvetica font, white text with black stroke on a transparent background
        text_input = textwrap.fill(text_input, width=25)
        size = (1080, 1000)
        font_color = (255, 255, 255)
        ttf_file = os.path.join(os.getcwd(), "Font\\coolvetica rg.otf")
        font = ImageFont.truetype(ttf_file, size=50)
        W, H = size
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        _, _, w, h = draw.textbbox((0, 0), text_input, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), text_input, font=font, fill=font_color, align="center", spacing=25,
                  stroke_width=4, stroke_fill="black")
        image.save(os.path.join(os.getcwd(), "Data_Cache\\Post_Title.png"))

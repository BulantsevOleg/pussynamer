from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from textwrap import wrap
import requests



def get_y_and_heights(text_wrapped, dimensions, margin, font):
    """Get the first vertical coordinate at which to draw text and the height of each line of text"""
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    # Calculate the height needed to draw each line of text (including its bottom margin)
    line_heights = [
        font.getmask(text_line).getbbox()[3] + descent + margin
        for text_line in text_wrapped
    ]
    # The last line doesn't have a bottom margin
    line_heights[-1] -= margin

    # Total height needed
    height_text = sum(line_heights)

    # Calculate the Y coordinate at which to draw the first line of text
    # y = (dimensions[1] - height_text) // 2
    y = (dimensions[1] - height_text) * 0.85

    # Return the first Y coordinate and a list with the height of each line
    return (y, line_heights)

def caption_img(caption):

    # Get image URL from response
    r = requests.get('https://api.thecatapi.com/v1/images/search?api_key=31564707-163b-413e-b7a2-f9727566957a')
    pussy_url = r.json()[0]["url"]
    # print(pussy_url)

    image = Image.open(requests.get(pussy_url, stream=True).raw)
    raw_image = image

    FONT_FAMILY = "rsc/Rubik/static/Rubik-Bold.ttf"
    CHAR_LIMIT = 14
    BG_COLOR = "black"
    TEXT_COLOR = "white"
    WIDTH, HEIGHT = image.size
    print(WIDTH, HEIGHT)
    V_MARGIN = 20
    FONT_SIZE = round(WIDTH / 10)
    # FONT_SIZE = 250
    

    font = ImageFont.truetype("rsc/Rubik/static/Rubik-Bold.ttf", size=FONT_SIZE)

    draw = ImageDraw.Draw(image)

    text_lines = wrap(caption, CHAR_LIMIT)
    print(text_lines)

    y, line_heights = get_y_and_heights(
        text_lines,
        (WIDTH, HEIGHT),
        V_MARGIN,
        font
    )

    for i, line in enumerate(text_lines):
        # Calculate the horizontally-centered position at which to draw this line
        line_width = font.getmask(line).getbbox()[2]
        x = ((WIDTH - line_width) // 2)
    
        # Draw this line
        draw.text((x, y), line, font=font, fill=TEXT_COLOR, stroke_width=2, stroke_fill=BG_COLOR)

        # Move on to the height at which the next line should be drawn at
        y += line_heights[i]

    # image.show()
    return(image)
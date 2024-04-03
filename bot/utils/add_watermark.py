from PIL import Image
from io import BytesIO


async def add_wm(img: BytesIO, watermark_buffer):
    main_img = Image.open(img)
    watermark = Image.open(watermark_buffer)

    watermark = watermark.resize((100, 100))

    transparency = 100

    watermark = watermark.convert('RGBA')
    watermark_with_transparency = Image.new('RGBA', watermark.size)
    for x in range(watermark.width):
        for y in range(watermark.height):
            r, g, b, a = watermark.getpixel((x, y))
            if not (r == 0 and g == 0 and b == 0):
                watermark_with_transparency.putpixel((x, y), (r, g, b, transparency))

    wm_pos = (10, 10)

    main_img.paste(watermark_with_transparency, wm_pos, watermark_with_transparency)

    return main_img

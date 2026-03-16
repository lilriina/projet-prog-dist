import math
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = "heart.png"

def heart_mask(width, height, center_x, center_y, size):
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    points = []
    for i in range(0, 360):
        t = math.radians(i)
        x = 16*math.sin(t)**3
        y = (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t))
        x = center_x + x*size
        y = center_y - y*size
        points.append((x, y))
    draw.polygon(points, fill=255)
    return mask

def create_gradient(width, height, color_top, color_bottom):
    gradient = Image.new("RGB", (width, height), color_top)
    for y in range(height):
        ratio = y / (height-1)
        r = int(color_top[0]*(1-ratio) + color_bottom[0]*ratio)
        g = int(color_top[1]*(1-ratio) + color_bottom[1]*ratio)
        b = int(color_top[2]*(1-ratio) + color_bottom[2]*ratio)
        ImageDraw.Draw(gradient).line([(0,y),(width,y)], fill=(r,g,b))
    return gradient

def scatter_sparkles(draw, width, height, mask, count=120):
    mask_pixels = mask.load()
    for _ in range(count):
        for _ in range(10):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if mask_pixels[x, y] > 128:
                r = random.randint(1, 3)
                draw.ellipse((x-r, y-r, x+r, y+r), fill="white")
                break

import math
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_PATH = "heart.png"

def heart_mask(width, height, center_x, center_y, size):
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    points = []
    for i in range(0, 360):
        t = math.radians(i)
        x = 16*math.sin(t)**3
        y = (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t))
        x = center_x + x*size
        y = center_y - y*size
        points.append((x, y))
    draw.polygon(points, fill=255)
    return mask

def create_gradient(width, height, color_top, color_bottom):
    gradient = Image.new("RGB", (width, height), color_top)
    for y in range(height):
        ratio = y / (height-1)
        r = int(color_top[0]*(1-ratio) + color_bottom[0]*ratio)
        g = int(color_top[1]*(1-ratio) + color_bottom[1]*ratio)
        b = int(color_top[2]*(1-ratio) + color_bottom[2]*ratio)
        ImageDraw.Draw(gradient).line([(0,y),(width,y)], fill=(r,g,b))
    return gradient

def scatter_sparkles(draw, width, height, mask, count=120):
    mask_pixels = mask.load()
    for _ in range(count):
        for _ in range(10):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            if mask_pixels[x, y] > 128:
                r = random.randint(1, 3)
                draw.ellipse((x-r, y-r, x+r, y+r), fill="white")
                break

def generate_heart_image(name: str, message: str, color_hex: str, path=OUTPUT_PATH):
    width, height = 900, 700
    background_color = "#FFF0F5"
    img = Image.new("RGB", (width, height), background_color)

    # Heart mask & gradient
    center_x, center_y = width//2, height//2 + 20
    size = 18
    mask = heart_mask(width, height, center_x, center_y, size)
    base_color = tuple(int(color_hex[i:i+2],16) for i in (1,3,5))
    gradient = create_gradient(width, height, base_color, (255,105,180))
    img.paste(gradient, (0,0), mask)

    draw = ImageDraw.Draw(img)
    scatter_sparkles(draw, width, height, mask, count=120)

    # Fonts - use try to load cute fonts
    try:
        font_name_path = "GreatVibes-Regular.ttf"
        font_msg_path = "Quicksand-VariableFont_wght.ttf"
    except:
        font_name_path = None
        font_msg_path = None

    # -----------------------
    # Adaptive name font
    # -----------------------
    heart_width = size*32  # roughly 32 units for x-range of heart
    max_name_width = heart_width*0.7  # leave padding
    text_size = 160
    while text_size > 20:
        try:
            font_name = ImageFont.truetype(font_name_path, text_size)
        except:
            font_name = ImageFont.load_default()
        bbox = draw.textbbox((0,0), name, font=font_name)
        text_width = bbox[2]-bbox[0]
        if text_width <= max_name_width:
            break
        text_size -= 5

    # -----------------------
    # Draw name
    # -----------------------
    bbox_name = draw.textbbox((0,0), name, font=font_name)
    name_w = bbox_name[2]-bbox_name[0]
    name_h = bbox_name[3]-bbox_name[1]
    name_x = width//2 - name_w//2
    name_y = center_y - 90  # lower for bigger heart

    shadow_offset = 2
    draw.text((name_x+shadow_offset, name_y+shadow_offset), name, font=font_name, fill="#FF99CC")
    draw.text((name_x, name_y), name, font=font_name, fill="#330033")

    # -----------------------
    # Adaptive message font
    # -----------------------
    msg_max_width = heart_width*0.6
    msg_size = 40
    while msg_size > 30:
        try:
            font_msg = ImageFont.truetype(font_msg_path, msg_size)
        except:
            font_msg = ImageFont.load_default()
        bbox = draw.textbbox((0,0), message, font=font_msg)
        msg_width = bbox[2]-bbox[0]
        if msg_width <= msg_max_width:
            break
        msg_size -= 5

    bbox_msg = draw.textbbox((0,0), message, font=font_msg)
    msg_w = bbox_msg[2]-bbox_msg[0]
    msg_h = bbox_msg[3]-bbox_msg[1]
    msg_x = width//2 - msg_w//2
    msg_y = center_y + 60  # lower for spacing

    draw.text((msg_x+shadow_offset, msg_y+shadow_offset), message, font=font_msg, fill="#FF99CC")
    draw.text((msg_x, msg_y), message, font=font_msg, fill="#330033")

    img.save(path)
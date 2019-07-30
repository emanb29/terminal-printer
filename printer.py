from PIL import Image
from math import trunc
from collections import Counter
from requests import get
from io import BytesIO

ENDC = '\033[0m'


def color_to_use(pixels):
    counted = Counter(pixels)
    return counted.most_common(1)[0][0]


def custom_text_color(tup):
    return (
        '\033[38;2;' +
        str(tup[0]) + ";" +
        str(tup[1]) + ";" +
        str(tup[2]) + 'm')


def custom_background(tup):
    return (
        '\033[48;2;' +
        str(tup[0]) + ";" +
        str(tup[1]) + ";" +
        str(tup[2]) + 'm')


def print_hole(url):
    # print(url)
    web = get(url)
    image = BytesIO(web.content)

    im = Image.open(image)
    x, y = im.size
    print(x, y)
    char_width = 120
    aspect_ratio = .413
    char_height = trunc(((y / x) * char_width) * aspect_ratio)

    pix_per_char_x = trunc(x / char_width)
    pix_per_char_y = trunc(y / char_height)

    print(pix_per_char_x)
    print(pix_per_char_y)

    to_print = []
    for i in range(char_height):
        colors = []
        for j in range(char_width):
            cur_char_top = []
            cur_char_bottom = []
            for k in range(pix_per_char_x):
                for l in range(trunc(pix_per_char_y/2)):
                    coord = (k + j * pix_per_char_x, l + i * pix_per_char_y)
                    im.getpixel(coord)
                    cur_char_top.append(im.getpixel(coord))
                for l in range(trunc(pix_per_char_y/2)):
                    coord = (k + j * pix_per_char_x, l +
                             trunc(pix_per_char_y/2) + i * pix_per_char_y)
                    im.getpixel(coord)
                    cur_char_bottom.append(im.getpixel(coord))
            common_top = color_to_use(cur_char_top)
            common_bottom = color_to_use(cur_char_bottom)
            colors.append(
                f"{custom_background(common_bottom)}{custom_text_color(common_top)}\u2580{ENDC}")
        to_print.append(colors)
    for i in to_print:
        print("".join(i))


# double_res()
# print_hole('https://pga-tour-res.cloudinary.com/image/upload/c_fill,w_720,b_rgb:424141,b_rgb:424242/holes_2018_r_464_552_overhead_green_18.jpg')


print_hole(
    'https://i.kym-cdn.com/entries/icons/original/000/018/012/this_is_fine.jpeg')

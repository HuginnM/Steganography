import os
from PIL import Image


def encode_image():
    text_mask = 0b10000000
    text_len = os.stat(text_file).st_size
    img_len = width * height

    if text_len > img_len:  # Определяем влезет ли текст в изображение
        print("Too long text")
        return False

    embed_len_text(text_file)

    while True:
        symbol = 0
        counter = 0
        for y in range(height):
            for x in range(width):
                if y == 0 and x < 32:  # Пропускаем сообщение о количестве
                    continue           # символов в тексте

                if counter % 8 == 0:        # Если весь символ был
                    symbol = text.read(1)   # закодирован - берём новый.

                    if not symbol:
                        print("Text has been encoded successfully")
                        return

                    symbol = ord(symbol)

                stego_bit = symbol & text_mask
                stego_bit >>= 7

                embed_color(x, y, stego_bit)
                symbol <<= 1
                counter += 1


def choose_rgb():
    chosen_rgb = int(input("Choose a color spectrum to encode:\n1 - Red;"
                           " 2 - Blue; 3 - Green:\n"))
    return chosen_rgb - 1


def embed(source_byte, stego_bit):
    if source_byte & 1 == stego_bit:
        return source_byte
    return source_byte ^ 1


#  Кодируем в начало изображения количество закодированных символов
def embed_len_text(txt_file):
    text_len = bin(os.stat(txt_file).st_size)
    text_len = text_len.replace('0b', '')
    text_len = '0'*(32 - len(text_len)) + text_len
    for x in range(32):
        embed_color(x, 0, int(text_len[x]))


# Функция принимает координаты пикселя и нужный бит для упаковки,
# после чего кодирует в выбранный ранее цветовой канал и изменяет пиксель.
def embed_color(x, y, stego_bit):
    new_color = [pix[x, y][0], pix[x, y][1], pix[x, y][2]]
    new_color[selected_rgb] = embed(pix[x, y][selected_rgb], stego_bit)
    new_color = tuple(new_color)
    image.putpixel((x, y), new_color)


image = Image.open('images/f35.bmp')  # Открываем изображение
text_file = 'sample.txt'
text = open(text_file, 'r')  # Открываем текст
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей
selected_rgb = choose_rgb()  # Выбираем спектр, в который будем кодировать

encode_image()

image.save("images/encoded.bmp", "bmp")
text.close()

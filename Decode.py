import os
import sys

BMP_HEADER_SIZE = 54


def decode_image(encoded_img, output_txt, symbols_to_read):
    img_mask = 0b11111110
    img_mask = ~img_mask
    img_len = os.stat(encoded_img).st_size
    selected_rgb = choose_rgb()

    if symbols_to_read >= img_len / 24 - BMP_HEADER_SIZE:
        print("Too much symbols to read")
        return False

    text = open(output_txt, 'w', encoding='utf-8')
    encoded_bmp = open(encoded_img, 'rb')

    encoded_bmp.seek(BMP_HEADER_SIZE + selected_rgb)

    read = 0
    while read < symbols_to_read:
        symbol = 0

        for bits_read in range(0, 8):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) &\
                       img_mask
            symbol <<= 1
            symbol |= img_byte
            encoded_bmp.seek(2, 1)

        if chr(symbol) == '\n' and len(os.linesep) == 2:
            read += 1

        read += 1
        print("Symbol #{0} is {1:c}".format(read, symbol))
        text.write(chr(symbol))

    text.close()
    encoded_bmp.close()
    return True


def choose_rgb():
    chosen_rgb = int(input("Choose a color spectrum to encode:\n1 - Red;"
                           " 2 - Blue; 3 - Green:\n"))
    return chosen_rgb - 1


to_read = int(input("How many characters are in the ciphertext?\n"))
image_file = "image/encoded.bmp"
decode_image(image_file, "result.txt", to_read)

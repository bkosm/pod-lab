import numpy as np
from PIL import Image
from bitstring import BitArray


def bitarrays_from_pixel(pixel: (int, int, int)) -> (BitArray, BitArray, BitArray):
    """ Convert a pixel tuple into accesible bit array objects.
    """
    r, g, b = pixel
    return BitArray(f'uintle:8={r}'), BitArray(f'uintle:8={g}'), BitArray(f'uintle:8={b}')


class LSB:
    def __init__(self, path: str):
        """ Open image from given path and prepare a pixel matrix
        """
        self.path = path
        self.image = Image.open(self.path)
        self.pixels = np.array(self.image)

    def encode(self, message: str, byte_fill=8, encoding='utf8', default_pos=-1) -> Image:
        """ Encode a rgb bitmap with specified message.
            If you're using a different encoding specify the byte_fill accordingly.
            It must be bigger or equal to that encoding's char size.
        """
        width, height = self.image.size
        encoded = np.ndarray(self.pixels.shape, dtype=np.uint8)

        msg_bits = [bin(char)[2:].zfill(byte_fill) for char in message.encode(encoding)] + ['0' * byte_fill]
        bits_gen = (c for c in ''.join(msg_bits))

        is_generator_empty = False
        for y in range(width):
            for x in range(height):
                if is_generator_empty:
                    encoded[x, y] = self.pixels[x, y]

                else:
                    rgb_bitarrays = bitarrays_from_pixel(self.pixels[x, y])

                    for color in rgb_bitarrays:
                        if not is_generator_empty and (bit := next(bits_gen, None)):
                            color.set(bit == '1', default_pos)
                        else:
                            is_generator_empty = True
                            break

                    r, g, b = rgb_bitarrays

                    encoded[x, y] = (r.uintle, g.uintle, b.uintle)  # get uint values of pixel colors

        return Image.fromarray(encoded)

    @staticmethod
    def decode(image: Image, byte_fill=8, encoding='utf8', default_pos=-1) -> str:
        """ Retrieve a message hidden in a rgb bitmap image.
        """
        width, height = image.size
        pixels = np.array(image)

        secrets = []
        counter = 0
        temp = ''
        for y in range(width):
            for x in range(height):
                rgb_bitarrays = bitarrays_from_pixel(pixels[x, y])

                for color in rgb_bitarrays:
                    temp += '1' if color[default_pos] else '0'
                    counter += 1

                    if counter == byte_fill:
                        byte = int(temp, 2)

                        if byte == 0:  # stop byte
                            return bytes(b for b in secrets).decode(encoding)

                        secrets += [byte]
                        temp = ''
                        counter = 0

        raise IndexError("no stop character in the entire image")


if __name__ == '__main__':
    img = LSB('./10_1.bmp')
    msg = 'Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie. Witam z wiadomości w obrazie.'

    encoded = img.encode(msg)
    encoded.show()

    print(LSB.decode(encoded))

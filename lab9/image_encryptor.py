from random import choice

import numpy as np
from PIL import Image

WHITE_BMP = 255
BLACK_BMP = 0


class BitmapEncryptor:
    def __init__(self, path: str):
        """ Open image from given path and prepare a pixel matrix
        """
        self.path = path
        self.image = Image.open(self.path)
        self.pixels = np.array(self.image)

    def peek(self) -> None:
        """ Open the loaded and processed image in current state in file browser.
        """
        Image.fromarray(self.pixels).show()

    def split_bitmap_in_two(self) -> (Image, Image):
        """ Split a bitmap into two encrypted images.
        """
        width, height = self.image.size
        share1, share2 = np.ndarray((height, width * 2)), np.ndarray((height, width * 2))
        white_variants = [(WHITE_BMP, BLACK_BMP), (BLACK_BMP, WHITE_BMP)]
        black_variants = [((WHITE_BMP, BLACK_BMP), (BLACK_BMP, WHITE_BMP)),
                          ((BLACK_BMP, WHITE_BMP), (WHITE_BMP, BLACK_BMP))]

        position = 0
        for x in range(height):
            for y in range(width):
                if self.pixels[x, y] < WHITE_BMP // 2:  # org is black
                    black1, black2 = choice(black_variants)  # random black combnation

                    share1[x, position] = black1[0]
                    share1[x, position + 1] = black1[1]
                    share2[x, position] = black2[0]
                    share2[x, position + 1] = black2[1]

                else:  # org is white
                    white1, white2 = choice(white_variants)  # random split combination for white pixel
                    share1[x, position] = white1
                    share1[x, position + 1] = white2
                    share2[x, position] = white1
                    share2[x, position + 1] = white2

                position += 2

            position = 0

        return Image.fromarray(share1), Image.fromarray(share2)

    @staticmethod
    def merge_two_bitmaps(image1: Image, image2: Image) -> Image:
        """ Merge two bitmaps into one to reveal the secret.
        """
        width, height = image1.size
        merged = np.ndarray((height, width))
        share1, share2 = np.array(image1), np.array(image2)

        for x in range(height):
            for y in range(width):
                if share1[x, y] == WHITE_BMP and share2[x, y] == WHITE_BMP:
                    merged[x, y] = WHITE_BMP
                else:
                    merged[x, y] = BLACK_BMP

        return Image.fromarray(merged)


if __name__ == '__main__':
    img = BitmapEncryptor('./2.bmp')

    share1, share2 = img.split_bitmap_in_two()

    share1.show()
    share2.show()

    BitmapEncryptor.merge_two_bitmaps(share1, share2).show()

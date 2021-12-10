import board
import neopixel

import time

def run():
    pixels = neopixel.NeoPixel(board.D18, 50)

    toggle = True
    while True:
        for i in range(len(pixels)):
            if ((i % 2) == 0) == toggle:
                pixels[i] = (0, 255, 0)
            else:
                pixels[i] = (255, 0, 0)
        
        print('flip!')
        toggle = not toggle


if __name__ == '__main__':
    run()


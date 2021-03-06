import ST7735



class lcdHelper:

    WIDTH = []
    HEIGHT = []
    def __init__(self):

        # Create ST7735 LCD display class
        self.st7735 = ST7735.ST7735(
            port=0,
            cs=1,
            dc=9,
            backlight=12,
            rotation=270,
            spi_speed_hz=10000000
        )
        # Initialize display
        self.st7735.begin()
        self.WIDTH = self.st7735.width
        self.HEIGHT = self.st7735.height


    def display(self, img):
        self.st7735.display(img)


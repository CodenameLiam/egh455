#!/usr/bin/env python3

import time
import colorsys
import sys
#import ST7735
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError, SerialTimeoutError
from enviroplus import gas
from subprocess import PIPE, Popen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging
from threading import Thread

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""combined.py - Displays readings from all of Enviro plus' sensors

Press Ctrl+C to exit!

""")



# Global array for sensor data
sensor_data = [0, 0, 0, 0, 0, 0, 0]

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()



# The position of the top bar
top_pos = 25

# Create a values dict to store the data
variables = ["temperature",
             "pressure",
             "humidity",
             "light",
             "oxidised",
             "reduced",
             "nh3"]

units = ["C",
         "hPa",
         "%",
         "Lux",
         "kO",
         "kO",
         "kO"]

# Define your own warning limits
# The limits definition follows the order of the variables array
# Example limits explanation for temperature:
# [4,18,28,35] means
# [-273.15 .. 4] -> Dangerously Low
# (4 .. 18]      -> Low
# (18 .. 28]     -> Normal
# (28 .. 35]     -> High
# (35 .. MAX]    -> Dangerously High
# DISCLAIMER: The limits provided here are just examples and come
# with NO WARRANTY. The authors of this example code claim
# NO RESPONSIBILITY if reliance on the following values or this
# code in general leads to ANY DAMAGES or DEATH.
limits = [[4, 18, 28, 35],
          [250, 650, 1013.25, 1015],
          [20, 30, 60, 70],
          [-1, -1, 30000, 100000],
          [-1, -1, 40, 50],
          [-1, -1, 450, 550],
          [-1, -1, 200, 300],
          [-1, -1, 50, 100],
          [-1, -1, 50, 100],
          [-1, -1, 50, 100]]

# RGB palette for values on the combined screen
palette = [(0, 0, 255),           # Dangerously Low
           (0, 255, 255),         # Low
           (0, 255, 0),           # Normal
           (255, 255, 0),         # High
           (255, 0, 0)]           # Dangerously High



class airQuality():
    values = {}
    def __init__(self, connection, WIDTH, HEIGHT):
        self.conn = connection
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        # Set up canvas and font
        self.img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.font_size_small = 10
        self.font_size_large = 20
        self.font = ImageFont.truetype(UserFont, self.font_size_large)
        self.smallfont = ImageFont.truetype(UserFont, self.font_size_small)
        self.x_offset = 2
        self.y_offset = 2

        self.message = ""

        # Tuning factor for compensation. Decrease this number to adjust the
        # temperature down, and increase to adjust up
        self.factor = 2.25

        self.cpu_temps = [self.get_cpu_temperature()] * 5

        self.delay = 0.5  # Debounce the proximity tap
        self.mode = 0    # The starting mode
        self.last_page = 0

        for v in variables:
            self.values[v] = [1] * self.WIDTH


    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self


    # Saves the data to be used in the graphs later and prints to the log
    def __save_data(self, idx, data):
        variable = variables[idx]
        # Maintain length of list
        self.values[variable] = self.values[variable][1:] + [data]
        unit = units[idx]
        message = "{}: {:.1f} {}".format(variable[:4], data, unit)
        logging.info(message)


    # Displays all the text on the 0.96" LCD
    def display_everything(self):
        self.draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), (0, 0, 0))
        column_count = 2
        row_count = (len(variables) / column_count)
        for i in range(len(variables)):
            self.variable = variables[i]
            self.data_value = self.values[self.variable][-1]
            sensor_data[i] = self.data_value
            self.unit = units[i]
            self.x = self.x_offset + ((self.WIDTH // column_count) * (i // row_count))
            self.y = self.y_offset + ((self.HEIGHT / row_count) * (i % row_count))
            self.message = "{}: {:.1f} {}".format(self.variable[:4], self.data_value, self.unit)
            self.lim = limits[i]
            self.rgb = palette[0]
            for j in range(len(self.lim)):
                if self.data_value > self.lim[j]:
                    self.rgb = palette[j + 1]
            self.draw.text((self.x, self.y), self.message, font=self.smallfont, fill=self.rgb)
        #st7735.display(img)
        #conn.sensor_message(sensor_data)


    # Get the temperature of the CPU for compensation
    def get_cpu_temperature(self):
        self.process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
        self.output, self._error = self.process.communicate()
        return float(self.output[self.output.index('=') + 1:self.output.rindex("'")])

    def getImage(self):
        return self.img

    def update(self):
        # The main loop
        try:
            while True:
                self.proximity = ltr559.get_proximity()

                # If the proximity crosses the threshold, toggle the mode
                # if self.proximity > 1500 and time.time() - self.last_page > self.delay:
                #     self.mode += 1
                #     self.mode %= (len(variables) + 1)
                #     self.last_page = time.time()

                # Display everything on the LCD screen
                if self.mode == 0:
                    # Temperature
                    self.cpu_temp = self.get_cpu_temperature()
                    # Smooth out with some averaging to decrease jitter
                    self.cpu_temps = self.cpu_temps[1:] + [self.cpu_temp]
                    self.avg_cpu_temp = sum(self.cpu_temps) / float(len(self.cpu_temps))
                    self.raw_temp = bme280.get_temperature()
                    self.raw_data = self.raw_temp - ((self.avg_cpu_temp - self.raw_temp) / self.factor)
                    self.__save_data(0, self.raw_data)
                    self.display_everything()
                    # Pressure
                    self.raw_data = bme280.get_pressure()
                    self.__save_data(1, self.raw_data)
                    self.display_everything()
                    # Humidity
                    self.raw_data = bme280.get_humidity()
                    self.__save_data(2, self.raw_data)
                    # Light
                    if self.proximity < 10:
                        self.raw_data = ltr559.get_lux()
                    else:
                        self.raw_data = 1
                    self.__save_data(3, self.raw_data)
                    self.display_everything()
                    # Gas
                    gas_data = gas.read_all()
                    self.__save_data(4, gas_data.oxidising / 1000)
                    self.__save_data(5, gas_data.reducing / 1000)
                    self.__save_data(6, gas_data.nh3 / 1000)
                    self.display_everything()

        # Exit cleanly
        except KeyboardInterrupt:
            sys.exit(0)


def main():
    from lcdHelper import lcdHelper
    from webServerConnection import webServerConnection

    lcdhelper = lcdHelper()
    conn = webServerConnection()
    aQ = airQuality(conn, lcdhelper.WIDTH, lcdhelper.HEIGHT)
    aQ.start()

    while True:
        sensor_img = aQ.getImage()
        lcdhelper.display(sensor_img)


if __name__ == "__main__":
    main()


import typing

import adafruit_displayio_ssd1306
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label

from Configuration import Configuration


class Display:
    
    _display: typing.Final[adafruit_displayio_ssd1306.SSD1306]
    _text_line_1: typing.Final[label.Label] = label.Label(terminalio.FONT, text="text line 1", y=5)
    _text_line_2: typing.Final[label.Label] = label.Label(terminalio.FONT, text="text line 2", y=15)
    _text_line_3: typing.Final[label.Label] = label.Label(terminalio.FONT, text="text line 3", y=25)

    def __init__(self, config: Configuration):
        dc = config.display
        i2c = board.I2C() if not dc.pins else busio.I2C(dc.pins.scl, dc.pins.sda)
        display_bus = displayio.I2CDisplay(i2c, device_address=dc.device_address)#, reset=board.D6)
        self._display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=dc.width, height=dc.height, rotation=dc.rotation)
        displayio.release_displays()
        labels = displayio.Group()
        self._display.show(labels)
        labels.append(self._text_line_1)
        labels.append(self._text_line_2)
        labels.append(self._text_line_3)
        super(Display, self).__init__(config)
        return self
        

    @property
    def text_line_1(self):
        return self._text_line_1.text
    @text_line_1.setter
    def text_line_1(self, value):
        self._text_line_1.text = value

    @property
    def text_line_2(self):
        return self._text_line_2.text
    @text_line_2.setter
    def text_line_2(self, value):
        self._text_line_2.text = value

    @property
    def text_line_3(self):
        return self._text_line_3.text
    @text_line_3.setter
    def text_line_3(self, value):
        self._text_line_3.text = value


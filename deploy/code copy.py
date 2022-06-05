import math
import time

import adafruit_displayio_ssd1306
import board
import displayio
import neopixel
import terminalio
import touchio
from adafruit_display_text import label
from analogio import AnalogIn, AnalogOut
from digitalio import DigitalInOut, Direction, Pull
from neopixel import NeoPixel


class MODE:
    Waiting = 1
    Setting = 2
    Zapping = 3
class COLORS:
    RED = 0
    YELLOW = 1/6
    LIME = 2/6
    CYAN = 3/6
    BLUE = 4/6
    MAGENTA = 5/6

    # h2r = lambda h,s,v: (lambda i: (lambda f: (lambda p: (lambda q: (lambda t: [(v, t, p),(q, v, p),(p, v, t),(p, q, v),(t, p, v),(v, p, q)][int(i%6)])(v * (1-(1-f)*s)))(v * (1-f*s)))(v * (1-s)))(h*6 - i))(math.floor(h*6))

    def hsv2rgb(h:float, s:float=1, v:int=255):
        i = math.floor(h*6)
        f = h*6 - i
        p = round(v * (1-s))
        q = round(v * (1-f*s))
        t = round(v * (1-(1-f)*s))

        return [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(i%6)]


displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)#, reset=board.D6)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)

 
pixel = NeoPixel(board.NEOPIXEL, 1, pixel_order=neopixel.GRB)
def set_color(hue,sat=1,brightness=1):
    pixel[0] = COLORS.hsv2rgb(hue, min(sat,1), min(brightness,1)*255)

led_builtin = DigitalInOut(board.LED)
led_builtin.direction = Direction.OUTPUT

ref_pin = AnalogOut(board.A0)
sense_pin = AnalogIn(board.A1)
gate_pin = AnalogIn(board.A3)
tool_pin = AnalogIn(board.A4)
adj_pin = AnalogIn(board.A5)
touch = touchio.TouchIn(board.D4)

def tween(current, next, factor=0.01):
    return current * (1-factor) + next * factor

sense_text = label.Label(terminalio.FONT, text="sense")
sense_text.x = 0
sense_text.y = 5
current_text = label.Label(terminalio.FONT, text="current")
gate_text = label.Label(terminalio.FONT, text="gate")
current_text.y=15
gate_text.y=25
labels = displayio.Group()
display.show(labels)
labels.append(sense_text)
labels.append(current_text)
labels.append(gate_text)

mode = MODE.Waiting
conv = 3.3/65520#35
rsense = 979#1459
rtooldiv = 646/66.6
vbaseline = 0.000_030 * rsense
vtarget = vbaseline
vadj = vbaseline
while True:
    led_builtin.value = touch.value
    vsense = sense_pin.value * conv
    vgate = gate_pin.value * conv
    vtool = tool_pin.value * conv# * rtooldiv
    touching = touch.value

    # vadj = tween(vadj, adj_pin.value * conv, 0.25)
    vadj = adj_pin.value * conv
    vtarget = tween(vtarget, vadj, 0.1) if touch.value else vbaseline
    


    ref_pin.value = int(vtarget / conv)

    something = vsense / vtarget 
    
    set_color(COLORS.LIME if something > 0.95 else COLORS.BLUE, brightness=.05)
        
    # time.sleep(.001)

    sense_text.text=" V:%0.3f/%0.3f/%0.3f" % (vsense, vtarget, vadj)
    current_text.text="mA:%0.3f/%0.3f/%0.3f" % (vsense * 1000 / rsense, vtarget * 1000 / rsense, vadj * 1000 / rsense)
    gate_text.text="\n%0.3fV\t%d%%\t%0.3fV" % (vtool, something * 100, vgate)
    
    print("%0.3f - %0.3f" % (vadj, vtarget))

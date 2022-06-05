try:
    from typing import Optional
except ImportError:
    pass

import board
from Device import Device
from Configuration import *

def initme(ctor, values:dict):
    result = ctor()
    result.__dict__ = values

class MODE:
    Waiting = 1
    Setting = 2
    Zapping = 3

dev = Device(initme(Configuration, {
    "pins": initme(PinConfiguration, {
        "adj": board.A5,
        "gate": board.A3,
        "ref": board.A0,
        "sense": board.A1,
        "tool": board.A4,
        "touch": board.D4, 
        "led": board.LED,
        "pixel": board.NEOPIXEL,
    }),
    "display": initme(DisplayConfiguration, {
        "device_address": 0x3d,
        "width": 128, 
        "height": 64, 
        "rotation": 180
    }),
    "rsense": 979,#1459,
    "rtooldiv": 646/66.6
}))



mode = MODE.Waiting




while True:
    dev.isledlit = dev.istouching
    if dev.istouching:
        dev.vref = dev.vref * 0.99 + dev.vadj * 0.01
    else:
        dev.vref = 0
        
    dev.text_line_1 = f" V:{dev.vsense}/{dev.vref}/{dev.vadj}"
    dev.text_line_2 = f"mA:{dev.isense * 1000}/{dev.get_rsense_current(dev.vref) * 1000}/{dev.get_rsense_current(dev.vadj) * 1000}"
    dev.text_line_2 = f"   {dev.vgate}-{dev.vtool}"

import math
from neopixel import ColorUnion
try:
    from typing import Final, Tuple, Union
    SimpleColor = Tuple[int, int, int]
    AlphaColor = Tuple[int, int, int, int]
    ColorUnion = Union[int, SimpleColor, AlphaColor]
except ImportError:
    pass

def constrain(min, value, max):
    return min(max(value, min), max)

class HSV:
    """
    Hue Saturation Value
      
    Attributes:
        hue (float): 0-1
        saturation (float): 0-1
        value (float): 0-1
    """

    RED = HSV(1/6)
    YELLOW = HSV(1/6)
    LIME = HSV(2/6)
    CYAN = HSV(3/6)
    BLUE = HSV(4/6)
    MAGENTA = HSV(5/6)

    def __init__(self, hue: flat, sat:float=1, val:float=1):
        self.hue = constrain(0, hue, 1)
        self.saturation = constrain(0, sat, 1)
        self.value = constrain(0, val, 1)

    _hue: float
    _saturation: float
    _value: float

    @property
    def hue(self)->int:
        return self._hue
        

    @property
    def saturation(self)->int:
        return self._saturation
        

    @property
    def value(self)->int:
        return self._value
    
    hue2 = property(lambda self: return self._hue)

    def withHue(self, hue: float):
        return HSV(hue, self._saturation, self._value)
    def withSaturation(self, saturation: float):
        return HSV(self._hue, saturation, self._value)
    def withValue(self, value: float):
        return HSV(self._hue, self._saturation, value)

    def brighten(self, percent):
        return self.withValue(self._value + self._value * percent)
    def saturate(self, percent):
        return self.withValue(self._saturation + self._saturation * percent)

    @property
    def characterization(self):
        return ['red', 'yellow', 'lime', 'cyan', 'blue', 'magenta'][int(self._hue * 6)]
        
    def toRgb(self)->SimpleColor:
        v = round(self._value*255)
        i = math.floor(self._hue*6)
        f = self._hue*6 - i
        p = round(v * (1-self._saturation))
        q = round(v * (1-f*self._saturation))
        t = round(v * (1-(1-f)*self._saturation))

        return [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(i%6)]


# class COLORS:
#     RED = 0
#     YELLOW = 1/6
#     LIME = 2/6
#     CYAN = 3/6
#     BLUE = 4/6
#     MAGENTA = 5/6

#     def hsv2rgb(h:float, s:float=1, v:int=255):
#         i = math.floor(h*6)
#         f = h*6 - i
#         p = round(v * (1-s))
#         q = round(v * (1-f*s))
#         t = round(v * (1-(1-f)*s))

#         return [
#             (v, t, p),
#             (q, v, p),
#             (p, v, t),
#             (p, q, v),
#             (t, p, v),
#             (v, p, q),
#         ][int(i%6)]


# class Color:
#     def __set_name__(self, owner, name):
#         self.public_name = name
#         self.private_name = '_' + name
#     def __get__(self, obj, objtype=None) -> ColorUnion:
#         pass
#     def __set__(self, owner, value: ColorUnion):
#         pass
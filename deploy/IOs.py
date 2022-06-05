
from analogio import AnalogIn, AnalogOut
from digitalio import DigitalInOut, Direction, Pull
from neopixel import RGB, ColorUnion, NeoPixel
from touchio import TouchIn

from Configuration import Configuration

try:
    from typing import Final, Tuple, Union
    ColorUnion = Union[int, Tuple[int, int, int], Tuple[int, int, int, int]]
except ImportError:
    pass

class IOs:
    CONV: Final[str] = 3.3/65520
    _adj: AnalogIn
    _gate: AnalogIn
    _sense: AnalogIn
    _tool: AnalogIn
    _touch: TouchIn
    _ref: AnalogOut
    _led: DigitalInOut
    _pixel: NeoPixel

    def __init__(self, config: Configuration):
        self._adj = AnalogIn(config.pins.adj)
        self._gate = AnalogIn(config.pins.gate)
        self._sense = AnalogIn(config.pins.sense)
        self._tool = AnalogIn(config.pins.tool)
        self._touch = TouchIn(config.pins.touch)
        self._ref = AnalogOut(config.pins.ref)
        self._led = DigitalInOut(config.pins.led)
        self._led.direction = Direction.OUTPUT
        self._pixel = NeoPixel(config.pins.pixel, 1, pixel_order=RGB)
        self.vref = 0
        super(IOs, self).__init__(config)

    @property
    def vadj(self) -> float:
        return self._adj.value * self.CONV
    @property
    def vgate(self) -> float:
        return self._gate.value * self.CONV
    @property
    def vsense(self) -> float:
        return self._sense.value * self.CONV
    @property
    def vtool(self) -> float:
        return self._tool.value * self.CONV

    @property
    def istouching(self) -> bool:
        return self._touch.value

    _vref_value: float
    @property
    def vref(self) -> float:
        return self._vref_value
    @vref.setter
    def vref(self, value: float):
        self._vref_value = value
        self._ref.value = int(value / self.CONV)

    @property
    def isledlit(self) -> bool:
        return self._led.value

    @isledlit.setter
    def isledlit(self, value: bool):
        self._led.value = value


    @property
    def pixel_color(self):
        return self._pixel[0]

    @pixel_color.setter
    def pixel_color(self, value:ColorUnion):
        self._pixel[0] = value

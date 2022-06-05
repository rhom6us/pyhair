

from collections import namedtuple

try:
    from typing import Optional

    from microcontroller import Pin
except ImportError:
    pass

class I2C_Pins:
    sda: Pin
    scl: Pin
class DisplayConfiguration:
    pins: Optional[I2C_Pins]
    device_address: int
    height: int
    width: int
    rotation: int
class PinConfiguration:
    adj: Pin
    gate: Pin
    ref: Pin
    sense: Pin
    tool: Pin
    touch: Pin
    led:  Optional[Pin]
    pixel: Optional[Pin]
class Configuration:
    pins: PinConfiguration
    display: DisplayConfiguration
    rsense: int
    rtooldiv: float





from Configuration import Configuration
from Display import Display
from IOs import IOs

try:
    from typing import Final
except ImportError:
    pass

class Device(Display, IOs):
    rsense: Final[int]
    rtooldiv: Final[float]

    def __init__(self, config:Configuration):
        self.rsense = config.rsense
        self.rtooldiv = config.rtooldiv
        super(Device, self).__init__(config)

    @staticmethod
    def get_rsense_current(self, v:float):
        return v / self.rsense

    @property
    def isense(self):
        return self.get_rsense_current(self.vsense)

    @property
    def vtool(self):
        return super().vtool * self.rtooldiv

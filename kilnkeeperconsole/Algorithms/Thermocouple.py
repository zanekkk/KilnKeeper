#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================

import board
import digitalio
import adafruit_max31855
import threading
import time
from kilnkeeperconsole.models import ActualKilnStatus

class Thermocouple(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.temperature = self.get_temperature()

    def run(self):
        while True:
            actual_stat = ActualKilnStatus.objects.get(id=1)
            actual_stat.actualTemperature = self.get_temperature()
            actual_stat.save()
            time.sleep(0.5)

    def get_temperature(self):
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)

        max31855 = adafruit_max31855.MAX31855(spi, cs)
        self.temperature = max31855.temperature
        return self.temperature


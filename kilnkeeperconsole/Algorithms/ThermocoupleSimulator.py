#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================

import kilnkeeperconsole.Algorithms.constants as constants
import threading
import time
from kilnkeeperconsole.models import ActualKilnStatus


class ThermocoupleSimulator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.temperature = 20
        self.time_step = constants.checking_frequency

    def run(self):
        while True:
            actual_stat = ActualKilnStatus.objects.get(id=1)
            actual_stat.actualTemperature = self.temperature
            actual_stat.save()
            time.sleep(0.5)
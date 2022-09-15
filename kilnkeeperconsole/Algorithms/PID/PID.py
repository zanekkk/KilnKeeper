#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================
import datetime

class PID(object):
    def __init__(self, Kp, Ki, Kd):
        self.P = 0
        self.D = 0
        self.I = 0
        self.Ki = Ki
        self.Kp = Kp
        self.Kd = Kd
        self.last_PID = 0
        self.previous_time = datetime.datetime.now()
        self.lastError = 0

    def compute(self, SP, PV):
        now = datetime.datetime.now()
        time_past = (now - self.previous_time).total_seconds()

        error = float(SP - PV)
        self.P = self.Kp * error
        self.I += (1 / self.Ki) * error * time_past
        self.D = self.Kd * (error - self.lastError) / time_past
        output = self.P + self.I + self.D
        self.last_PID = output
        window = 100
        if output > window:
            output = window
        elif output <= 0:
            output = 0
        output = float(output / window)

        self.lastError = error
        self.previous_time = now
        return output

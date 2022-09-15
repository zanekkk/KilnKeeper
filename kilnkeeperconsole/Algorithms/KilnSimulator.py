#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================

import time
import kilnkeeperconsole.Algorithms.constants as constants
import kilnkeeperconsole.Algorithms.Kiln as Kiln
import kilnkeeperconsole.Algorithms.ThermocoupleSimulator as ThermocoupleSimulator
import datetime


class KilnSimulator(Kiln.Kiln):
    def __init__(self):
        self.thermocouple = ThermocoupleSimulator.ThermocoupleSimulator()
        self.t_environment = constants.temperature_of_environment
        self.coil_capacity = constants.coil_capacity
        self.kiln_capacity = constants.kiln_capacity
        self.coil_power = constants.coil_power
        self.kiln_env_resistance = constants.kiln_env_resistance
        self.coil_kiln_resistance = constants.coil_kiln_resistance
        self.plot_kilnTemperature = []
        self.plot_PID = []
        self.coil_on = 0
        self.coil_off = 0
        self.plot_time = []
        self.kiln_temp, self.coil_temp = self.t_environment, self.t_environment
        super().__init__()
        print("SimulatedOven started")

    def inside_kiln_simulation(self):
        self.coil_temp += (self.coil_power * self.frequency * self.pid_value) / self.coil_capacity
        self.coil_kiln_heat_change = (self.coil_temp - self.kiln_temp) / self.coil_kiln_resistance
        heat_change_in_time = self.frequency * self.coil_kiln_heat_change
        self.coil_temp -= heat_change_in_time / self.coil_capacity
        self.kiln_temp += heat_change_in_time / self.kiln_capacity
        self.kiln_env_heat_change = (self.kiln_temp - self.t_environment) / self.kiln_env_resistance
        self.kiln_temp -= self.frequency * self.kiln_env_heat_change / self.kiln_capacity
        self.temperature = self.kiln_temp
        self.thermocouple.temperature = self.kiln_temp

    def control_ssr(self):
        self.pid_value = self.pid.compute(self.target_interval_temperature,
                                          self.thermocouple.temperature)
        self.coil_on = float(self.frequency * self.pid_value)
        self.coil_off = float(self.frequency * (1 - self.pid_value))

        self.inside_kiln_simulation()

        print("simulation: -> %dW heater: %.0f -> %dW oven: %.0f -> %dW env" % (int(self.coil_power * self.pid_value),
                                                                                self.coil_temp,
                                                                                int(self.coil_kiln_heat_change),
                                                                                self.kiln_temp,
                                                                                int(self.kiln_env_heat_change)))

        time_left = self.total_time - self.run_time

        actual_time = datetime.datetime.now() - self.schedule_beginning_time
        actual_time = actual_time.total_seconds()
        # self.plot_kilnTemperature.append(self.kiln_temp)
        # self.plot_PID.append(self.coil_on)
        # self.plot_time.append(actual_time)
        self.set_actual_stat(self.kiln_temp)
        self.firing_time_minutes = actual_time

        try:
            print(
                " error=%.2f | pid=%.2f | p=%.2f | i=%.2f | d=%.2f | coil_on=%.2f | coil_off=%.2f | run_time=%d" %
                (self.pid.lastError,
                 self.pid.last_PID,
                 self.pid.P,
                 self.pid.I,
                 self.pid.D,
                 self.coil_on,
                 self.coil_off,
                 actual_time))
        except KeyError:
            pass

        time.sleep(self.frequency)

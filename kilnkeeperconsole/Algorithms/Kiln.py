#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================

import threading
import time
import datetime
import kilnkeeperconsole.Algorithms.constants as constants
from kilnkeeperconsole.Algorithms.PID.PID import PID
import matplotlib.pyplot as plt
from kilnkeeperconsole.models import Firing, History, KilnSettings, Schedule, ActualKilnStatus


class Kiln(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_id = threading.get_ident()
        self.temperature = 0
        self.frequency = constants.checking_frequency
        self.schedule = None
        self.schedule_beginning_time = 0
        self.start_time = 0
        self.run_time = 0
        self.total_time = 0
        self.target_interval_temperature = 0
        self.final_temperature = 0
        self.heat = 0
        self.coil_on = 0
        self.coil_of = 0
        self.firing_time_minutes = 0
        self.pid = PID(constants.pid_kp, constants.pid_ki, constants.pid_kd)
        self.running_schedule = False
        self.History = None
        # for real kiln
        # self.thermocouple = Thermocouple.Thermocouple()
        # self.thermocouple.start()

    def set_new_values(self):
        self.schedule = None
        self.History = None
        self.start_time = 0
        self.run_time = 0
        self.total_time = 0
        self.target_interval_temperature = 0
        self.final_temperature = 0
        self.heat = 0
        self.pid = PID(constants.pid_kp, constants.pid_ki, constants.pid_kd)

    def run_schedule(self, schedule):
        self.set_new_values()
        self.run_time = self.start_time
        self.schedule_beginning_time = datetime.datetime.now()
        self.start_time = datetime.datetime.now()
        self.schedule = schedule
        self.create_history()
        self.total_time = schedule.get_final_time()
        self.running_schedule = True
        print("======= Running schedule %s =========" % (schedule.name))

    def stop_schedule(self):
        self.running_schedule = False
        self.set_new_values()
        Firing.objects.all().delete()

    def check_kiln_temperature(self):
        temp = self.thermocouple.temperature
        temp_diff = abs(self.target_interval_temperature - temp)
        if temp_diff > constants.pid_admissible_difference:
            self.start_time = datetime.datetime.now() - datetime.timedelta(milliseconds=self.run_time * 1000)

    def update_runtime(self):
        runtime_diff = datetime.datetime.now() - self.start_time
        runtime_diff = datetime.timedelta(0) if runtime_diff.total_seconds() < 0 else runtime_diff
        self.run_time = runtime_diff.total_seconds()

    def set_interval_temperature(self):
        self.update_runtime()
        self.target_interval_temperature = self.schedule.calculate_next_interval_temperature(self.run_time)

    def reset_if_schedule_ended(self):
        plt.xlabel("Czas [min]")
        plt.ylabel('Temperatura [C]')
        if constants.run_over_time:
            if self.run_time > self.total_time and self.thermocouple.temperature != self.schedule.get_final_temperature():
                print("Program run time exceeded, run_over_time set to hit temperature anyway.")
            elif self.run_time > self.total_time and self.thermocouple.temperature == self.schedule.get_final_temperature():
                # print("============== SCHEDULE ENDED ================== ")
                # plt.plot(self.plot_time, self.plot_kilnTemperature)
                # plt.show()

                self.set_firing_cost()
                self.stop_schedule()
        else:
            if self.run_time > self.total_time:
                # print("============== SCHEDULE ENDED ================== ")
                # print(self.plot_time)
                # print(self.plot_kilnTemperature)
                # print(self.plot_PID)
                # plt.plot(self.plot_time, self.plot_kilnTemperature)
                # plt.show()
                self.set_firing_cost()
                self.stop_schedule()

    def add_to_firing_history(self):
        new_firing_save = Firing()
        new_firing_save.temp = self.temperature
        new_firing_save.target = self.target_interval_temperature
        new_firing_save.error = self.pid.lastError
        new_firing_save.p = self.pid.P
        new_firing_save.i = self.pid.I
        new_firing_save.d = self.pid.D
        new_firing_save.pid = self.pid.last_PID
        new_firing_save.coil_on = self.coil_on
        new_firing_save.coil_of = self.coil_of
        new_firing_save.firing_time = self.run_time
        time_left = self.total_time - self.run_time
        new_firing_save.time_left = time_left
        new_firing_save.History = self.History
        new_firing_save.save()

    def control_ssr_live(self):
        pid = self.pid.compute(self.target_interval_temperature,
                               self.thermocouple.temperature)
        heat_on = float(self.frequency * pid)
        heat_off = float(self.frequency * (1 - pid))

        actual_time = datetime.datetime.now() - self.schedule_beginning_time
        actual_time = actual_time.total_seconds() / 60
        # self.plot_kilnTemperature.append(self.kiln_temp)
        # self.plot_PID.append(self.coil_on)
        # self.plot_time.append(actual_time)
        self.firing_time_minutes = actual_time
        if heat_on:
            self.ssr_on(heat_on)
        if heat_off:
            self.ssr_off(heat_off)

        self.set_actual_stat(self.thermocouple.temperature)


    def ssr_on(self, pwm):
        self.GPIO.output(27, self.GPIO.HIGH)
        time.sleep(pwm)

    def ssr_off(self, pwm):
        self.GPIO.output(27, self.GPIO.LOW)
        time.sleep(pwm)

    def run(self):
        while True:
            if self.running_schedule:
                self.check_kiln_temperature()
                self.set_interval_temperature()

                # control_ssr - simulation
                # control_ssr_live - real
                self.control_ssr()
                # self.control_ssr_live()

                self.add_to_firing_history()
                self.reset_if_schedule_ended()

    def create_history(self):
        self.History = History()
        self.History.Schedule = Schedule.objects.get(id=self.schedule.schedule_id)
        s = KilnSettings.objects.get(id=1)
        self.History.date = datetime.datetime.now()
        self.History.note = ' '
        self.History.save()

    def set_firing_cost(self):
        s = KilnSettings.objects.get(id=1)
        firing_cost = (self.firing_time_minutes / 60) * s.Kiln_power * s.kWh_cost
        self.History.cost = firing_cost
        self.History.save()

    def set_actual_stat(self,temp):
        ActualKilnStatus.objects.select_for_update().filter(id=1).update(actualTemperature=temp, firing=self.running_schedule, schedule_id=self.schedule.schedule_id)


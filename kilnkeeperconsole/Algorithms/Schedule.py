#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================

from kilnkeeperconsole.models import Step


class Schedule:
    def __init__(self, scheduleDB):
        self.name = scheduleDB.name
        stepList = list(Step.objects.filter(Schedule_id=scheduleDB.id).values_list())
        self.schedule_id = scheduleDB.id
        self.data = []
        for idx, l in enumerate(stepList):
            self.data.append([l[3], l[4]])

    def temperatures_between_steps(self, time):
        if time > self.get_final_time():
            return None, None
        prev_temp = None
        next_temp = None
        for i in range(len(self.data)):
            if time < self.data[i][0]:
                prev_temp = self.data[i - 1]
                next_temp = self.data[i]
                break

        return prev_temp, next_temp

    def calculate_next_interval_temperature(self, time):
        if time > self.get_final_time():
            return 0

        (prev_temp, next_temp) = self.temperatures_between_steps(time)
        previous_step_temperature = prev_temp[1]
        previous_step_time = prev_temp[0]
        next_step_temperature = next_temp[1]
        next_step_time = next_temp[0]
        time_between_steps = float(next_step_time - previous_step_time)
        degrees_between_steps = float(next_step_temperature - previous_step_temperature)

        degrees_per_second = degrees_between_steps / time_between_steps
        degrees_by_actual_step = (time - previous_step_time) * degrees_per_second
        interval_temperature = previous_step_temperature + degrees_by_actual_step
        return interval_temperature

    def get_final_temperature(self):
        return self.data[len(self.data) - 1][1]

    def get_final_time(self):
        return self.data[len(self.data) - 1][0]

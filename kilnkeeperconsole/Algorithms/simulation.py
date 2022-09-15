#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================

# Class used for testing and ploting PID and kiln
import kilnkeeperconsole
import kilnkeeperconsole.Algorithms.KilnSimulator as KilnSimulator
import kilnkeeperconsole.Algorithms.Schedule as Schedule
import json
import os
from kilnkeeperconsole.models import Schedule as ScheduleDB
from kilnkeeperconsole.models import Step
from django.conf import settings

schedule = ScheduleDB(name="cone-6")  # create a ToDoList
schedule.save()



kiln = KilnSimulator.KilnSimulator()
schedule_json = json.dumps(schedule)
scheduleDB = ScheduleDB.objects.get(name="cone-6")
schedule = Schedule.Schedule(scheduleDB)
kiln.run_schedule(schedule)




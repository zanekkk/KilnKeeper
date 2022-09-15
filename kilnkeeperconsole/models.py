#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================

from django.db import models


class Schedule(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Step(models.Model):
    Schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    numerInLine = models.IntegerField()
    minutes = models.IntegerField()
    temperature = models.IntegerField()

    def __str__(self):
        return self.temperature


class History(models.Model):
    Schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    cost = models.FloatField(default=None, blank=True, null=True)
    date = models.DateTimeField()
    note = models.CharField(max_length=500)
    def __str__(self):
        return self.note


class KilnSettings(models.Model):
    Kp = models.IntegerField()
    Ki = models.IntegerField()
    Kd = models.IntegerField()
    Interval = models.FloatField()
    Max_kiln_temperature = models.IntegerField(default=None, blank=True, null=True)
    Kiln_power = models.IntegerField(default=None, blank=True, null=True)
    kWh_cost = models.FloatField(default=None, blank=True, null=True)


class Firing(models.Model):
    History = models.ForeignKey(History, on_delete=models.CASCADE, related_name='+')
    temp = models.FloatField()
    target = models.FloatField()
    error = models.FloatField()
    p = models.FloatField()
    i = models.FloatField()
    d = models.FloatField()
    pid = models.FloatField()
    coil_on = models.FloatField()
    coil_of = models.FloatField()
    firing_time = models.FloatField()
    time_left = models.FloatField()

    def __str__(self):
        return self.temp


class ActualKilnStatus(models.Model):
    actualTemperature = models.FloatField()
    firing = models.BooleanField()
    schedule_id = models.IntegerField(default=None, blank=True, null=True)


#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from kilnkeeperconsole.models import KilnSettings, Step, Schedule, ActualKilnStatus, History, Firing
import kilnkeeperconsole.Algorithms.Schedule as ScheduleAlg
import kilnkeeperconsole.Algorithms.KilnSimulator as KilnSimulator

kiln = KilnSimulator.KilnSimulator()
# kiln = Kiln.Kiln()

def home(request):
    act = ActualKilnStatus.objects.get(id=1)
    schedule = Schedule.objects.get(id=act.schedule_id)
    latest_history = History.objects.latest('id')
    data = []
    labels = []
    firings = Firing.objects.filter(History_id=latest_history.id).all().order_by('id')
    for firing in firings:
        labels.append(firing.firing_time)
        data.append(firing.temp)

    return render(request, 'kilnkeeperconsole/home.html',
                  {'actual': act, 'schedule': schedule, 'labels': labels, 'data': data})


def settings(request):
    settings = KilnSettings.objects.get(id=1)
    act = ActualKilnStatus.objects.first()
    if request.method == 'POST':
        settings.kWh_cost = request.POST['kWhCost'] if request.POST['kWhCost'] != None else settings.kWh_cost
        settings.Max_kiln_temperature = request.POST['maxTemperature'] if request.POST[
                                                                              'maxTemperature'] is not None else settings.Max_kiln_temperature
        settings.Kiln_power = request.POST['kilnPower'] if request.POST[
                                                               'kilnPower'] is not None else settings.Kiln_power
        settings.Interval = request.POST['Interval'] if request.POST['Interval'] is not None else settings.Interval
        settings.Kd = request.POST['Kd'] if request.POST['Kd'] is not None else settings.Kd
        settings.Kp = request.POST['Kp'] if request.POST['Kp'] is not None else settings.Kp
        settings.Ki = request.POST['Ki'] if request.POST['Ki'] is not None else settings.Ki
        settings.save()
    return render(request, 'kilnkeeperconsole/settings.html', {'settings': settings, 'actual': act})


def new_schedule(request):
    act = ActualKilnStatus.objects.first()
    return render(request, 'kilnkeeperconsole/newSchedule.html', {'actual': act})


def schedules(request):
    act = ActualKilnStatus.objects.first()
    schedules = Schedule.objects.all()
    return render(request, 'kilnkeeperconsole/schedules.html', {'actual': act, 'schedules': schedules})


def history(request):
    act = ActualKilnStatus.objects.first()
    history = History.objects.all()
    return render(request, 'kilnkeeperconsole/history.html', {'actual': act, 'history': history})


def stop_firing(request):
    kiln.stop_schedule()
    return redirect('kilnkeeperconsole/schedules.html')


def schedule(request, schedule_id):
    act = ActualKilnStatus.objects.first()
    scheduleDB = Schedule.objects.get(id=schedule_id)
    steps = Step.objects.filter(Schedule_id=scheduleDB.id).all()
    return render(request, 'kilnkeeperconsole/schedule.html', {'schedule': scheduleDB, 'steps': steps, 'actual': act})


def delete_schedule(request, schedule_id):
    scheduleDB = Schedule.objects.get(id=schedule_id)
    scheduleDB.delete()
    return render(request, 'kilnkeeperconsole/schedules.html', {'schedule': scheduleDB})


def add_schedule(request):
    act = ActualKilnStatus.objects.first()
    schedule = Schedule()
    schedule.name = 'New schedule'
    schedule.save()
    max_temp = KilnSettings.objects.get(id=1).Max_kiln_temperature
    return render(request, 'kilnkeeperconsole/newSchedule.html', {'actual': act, 'schedule': schedule, 'max_temp' : max_temp})


def add_step(request, schedule_id, minutes, temperature):
    act = ActualKilnStatus.objects.first()
    step = Step()
    step.Schedule = Schedule.objects.get(id=schedule_id)
    step.minutes = minutes
    step.temperature = temperature
    step.numerInLine = Step.objects.filter(schedule_id=schedule_id).all().count() + 1
    print(Step.objects.filter(schedule_id=schedule_id).all().count())
    step.save()
    steps = Step.objects.filter(schedule_id=schedule_id).all()
    return render(request, 'kilnkeeperconsole/newSchedule.html', {'actual': act, 'schedule': schedule, 'steps': steps})


def history_detail(request, id):
    history = History.objects.get(id=id)
    act = ActualKilnStatus.objects.first()
    data = []
    labels = []
    firings = Firing.objects.filter(History_id=history.id).all().order_by('id')
    for firing in firings:
        labels.append(firing.firing_time)
        data.append(firing.temp)
    return render(request, 'kilnkeeperconsole/history_detail.html', {'actual': act, 'history': history, 'labels': labels, 'data': data})


def history_specific_detail(request, id):
    history = History.objects.filter(Schedule_id=id).all()
    act = ActualKilnStatus.objects.first()
    return render(request, 'kilnkeeperconsole/history.html', {'actual': act, 'history': history})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "kilnkeeperconsole/home.html")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('login')

    return render(request, 'kilnkeeperconsole/login.html', {})


def logout_page(request):
    return render(request, 'kilnkeeperconsole/login.html', {})


def run_schedule(request, id):
    scheduleDB = Schedule.objects.get(id=id)
    if not kiln.is_alive():
        kiln.start()
    schedule = ScheduleAlg.Schedule(scheduleDB)
    kiln.run_schedule(schedule)
    ActualKilnStatus.objects.select_for_update().filter(id=1).update(schedule_id=id)
    return redirect('/')

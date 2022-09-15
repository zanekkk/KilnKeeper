#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='console-home'),
    path('settings/', views.settings, name='console-settings'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('new_schedule/', views.new_schedule, name='new_schedules'),
    path('schedules/', views.schedules, name='schedules'),
    path('history/', views.history, name='history'),
    path('stop_firing/', views.stop_firing, name='stop_firing'),
    path('schedule/<schedule_id>/', views.schedule, name='schedule'),
    path('edit_schedule/', views.new_schedule, name='edit_schedule'),
    path('delete_schedule/<schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    path('add_step/', views.add_step, name='add_step'),
    path('history_detail/<id>/', views.history_detail, name='history_detail'),
    path('history/<id>/', views.history_specific_detail, name='history_specific_detail'),
    path('run_schedule/<id>/', views.run_schedule, name='run_schedule')
]

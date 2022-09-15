#           Żaneta Pająk 2022
#       Kod źródłowy do pracy dyplomowej
# - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - -
#   Temat: Stworzenie zaawansowanego kontrolera pieca
#      do wypału ceramiki z wykorzystaniem RaspberryPi
# ==================================================================================================
######### KILN SIMULATOR CONSTANTS #############
temperature_of_environment      = 20.0      # C
coil_power                      = 5000      # W
coil_capacity                   = 318.0     # J/K
coil_kiln_resistance            = 0.1        # K/W
kiln_capacity                   = 4000.0     # J/K
kiln_env_resistance             = 0.21      # K/W
checking_frequency              = 2         # s

######### PID CONSTANTS #############
pid_kp = 150
pid_ki = 90
pid_kd = 90
pid_admissible_difference = 3

run_over_time = False

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 12 aug 2022
#--------------------------------------------------------

#  This file contains the implementation of the system
#  functions related to POWER MANAGEMENT.


# take a look at this: https://stackoverflow.com/questions/23013274/shutting-down-computer-linux-using-python


import os


# list of accepted events
events = ['POWER_OFF', 'POWER_REBOOT', 'POWER_STATUS']

def poweroff() -> None:
    os.system('systemctl poweroff')

def reboot() -> None:
    os.system('systemctl reboot -i')

def status() -> str:
    return 'vuoi na canzone?'

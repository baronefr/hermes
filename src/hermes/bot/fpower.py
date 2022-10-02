
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 12 aug 2022
#--------------------------------------------------------

#  This file contains the implementation of the system
#  functions related to POWER MANAGEMENT.


# take a look at this: https://stackoverflow.com/questions/23013274/shutting-down-computer-linux-using-python


import os
import subprocess
import psutil, datetime

# list of accepted events
events = ['POWER_OFF', 'POWER_REBOOT', 'POWER_STATUS']

def poweroff() -> None:
    os.system('systemctl poweroff')

def reboot() -> None:
    os.system('systemctl reboot -i')


def status() -> list:
    try:
        # last system boot
        last_boot = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    except: last_boot = 'err'
    
    try:
        # who -u   logged users
        logged_users = subprocess.Popen(["who","-u"], cwd="/", stdout=subprocess.PIPE).stdout.read().decode()
    except: logged_users = 'err'
    
    try:
        # free -h
        free_memory = subprocess.Popen(["free","-h"], cwd="/", stdout=subprocess.PIPE).stdout.read().decode()
        # --- but format it in a better way!
        mem_msg = ''
        for line in free_memory.splitlines():
            ll = line.split()
            if ll[0] == 'total':  mem_msg += "    (" + ", ".join(ll[0:3]) + ')\n'
            else: mem_msg += " | ".join(ll[0:4]) + '\n'
    except: mem_msg = 'err'
    
    # cpu usage
    cpu_usage = psutil.cpu_percent()
    
    # temp sensors
    try:
        temp_msg = ''
        temps = psutil.sensors_temperatures()
        if not temps:  print("can't read any temperature")
        for kk, vv in temps.items():
            temp_msg = temp_msg + """{} : {}\n""".format(kk, str(vv[0].current))
    except: temp_msg = 'err'
    
    # send as separate messages (only this case! TODO: generalize to any return value)
    return [
             """\[*boot*] {}""".format(last_boot),
             """\[*logged users*]\n {}""".format(logged_users),
             """\[*memory*] {}""".format(mem_msg),
             """\[*cpu*] {}%\n""".format( cpu_usage ),
             """\[*temperatures*] \n{}""".format( temp_msg ),
           ]


#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 02 Oct 2022
#--------------------------------------------------------


#   -->  EXTERNAL FUNCTIONS -------------------------------
#  This file allows you to easily create custom commands for the bot, which perform some
#  actions on the systems and return a callback string. We distinguish between:
#   - oneshot commands: send a message to the bot and get an answer
#   - query: send a message, get a reply menu with many options & pick one
#
#  Eventually you have to activate these functions in your settings.ini:
#  ........................
#  [external]
#  oneshot=bonjour,netstat
#  query=rgb
#  ........................
#


import urllib.request
import subprocess


##   ONESHOT ----------------------------------------------

#  remark: A special oneshot message is bonjour, which follows
#          the default bonjur message.
def bonjour() -> str:
    """bonjour message"""  # <- docstrings are used to compose the help menu
    return "Something you want to say after bonjour?"


#  this is an example of oneshot command, which sends network informations
def netstat() -> str:
    """network status"""
    
    try:
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        interface = subprocess.Popen("iwgetid", cwd="/", stdout=subprocess.PIPE).stdout.read().decode()
        hostIP = subprocess.Popen(["hostname","-I"], cwd="/", stdout=subprocess.PIPE).stdout.read().decode()
        message = """\[extIP] {}\n\[route] {}\n\[interface] {}""".format(external_ip, hostIP.rstrip(), interface.rstrip())
    except Exception as err:
        message = f"netstat error:\n{err}"
        print(' [err] netstat', err)
    return message



##   QUERY ------------------------------------------------

class rgb:
    """ 💡 OpenRGB query"""
    
    # markup menu
    msg = "💡 OpenRGB: pick a color"
    #     [i]  remark: menu is a list of couples ('menu name', 'callback string')
    menu = [
             ("🟡 yellow", 'YEL'),
             ("🔴 red",    'RED'),
             ("🟢 green",  'GRE'),
             ("🔵 blue",   'BLU'),
             ("⚫ off",    'OFF')
           ]
    
    # action handler - execute your action, send back a txt
    def event(event = '') -> str:
        # [i] execute what you want based on callback string
        msg = 'none'
        
        if event == 'YEL':
            msg = 'yellow'
            
        elif event == 'RED':
            msg = 'yellow'
            
        elif event == 'GRE':
            msg = 'green'
            
        elif event == 'BLU':
            msg = 'blue'
            
        elif event == 'OFF':
            msg = 'poweroff'
        
        return('OpenRGB ->' + event)

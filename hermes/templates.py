
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 22 Feb 2022
#--------------------------------------------------------

setup_template = """hostname={}
token={}
chatid={}
userid={}"""

settings_template = """[general]
hostname={}
token={}

[bot]
log_dir=log/
unauthorized_ghosting=true
unknown_command_ignore=true

[task]
task_path=/tmp/hermes/
default_user=0

[modules]
oneshot=netstat
query=None"""

auth_template = "chatid,name,bonjour,active\n"
env_template = "\n# private hermes env\nexport {}=\"{}\"\n"





external_template = """
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
    \"\"\"bonjour message\"\"\"  # <- docstrings are used to compose the help menu
    return "Something you want to say after bonjour?"

#  this is an example of oneshot command, which sends network informations
def netstat() -> str:
    \"\"\"network status\"\"\"
    
    try:
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        interface = subprocess.Popen("iwgetid", cwd="/", stdout=subprocess.PIPE).stdout.read().decode()
        hostIP = subprocess.Popen(["hostname","-I"], cwd="/", stdout=subprocess.PIPE).stdout.read().decode()
        message = \"\"\"\[extIP] {}\n\[route] {}\n\[interface] {}\"\"\".format(external_ip, hostIP.rstrip(), interface.rstrip())
    except Exception as err:
        message = f"netstat error: {err}"
        print(' [err] netstat', err)
    return message



##   QUERY ------------------------------------------------

# To see a custom query implementation, look at lib/external.py
"""




systemd_template = """[Unit]
Description=Hermes host
After=network-online.target

[Service]
Type=simple
User={}
Group={}
Environment={}
ExecStart={}
Restart=on-failure
RestartSec=120

[Install]
WantedBy=multi-user.target
"""
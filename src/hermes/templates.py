
#########################################################
#   HERMES - github.com/baronefr/hermes
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





extra_template = """
#########################################################
#   HERMES - telegram bot for messages & system control
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 30 Aug 2023
#--------------------------------------------------------


#   -->  EXTERNAL FUNCTIONS -------------------------------
#  This file allows you to easily create custom oneshot commands for the bot. A oneshot command is
#  a function that can be executed and returns callback string, which is sent to the user.
#
#  Code here your function, then open your settings file and add the function with the oneshot flag:
#  ........................
#  [modules]
#  oneshot=bonjour,yourfunction
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
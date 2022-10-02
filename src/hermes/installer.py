
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 01 Oct 2022
#--------------------------------------------------------

import os
import sys
import socket
import getpass

import configparser

import hermes
from hermes.common import *


##  IO ----------------------------------------------------

setup_file = hermes.common.namespace['SETUP_FILE']
settings_file = hermes.common.namespace['SETTINGS_FILE']
auth_file = hermes.common.namespace['AUTH_FILE']
ext_file = hermes.common.namespace['EXTERNAL_EXE']

##  TEMPLATES ---------------------------------------------

# setup file template
setup_template = """hostname={}
token={}
chatid={}
userid={}
"""

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

[external]
oneshot=netstat
query=None
"""

auth_template = "chatid,name,bonjour,active\n"


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



##  lib ---------------------------------------------------

# create a new blank setup file, to be edited by the user
def new_setup(prefix = '') -> None:
    
    try:
        # get user details
        hostname = socket.gethostname()
        username = getpass.getuser()
    except Exception as e:
        print(" [ err ] cannot retrieve session details")
        print(e)
        pass
    
    # print file for setup arguments
    try:
        f = open( prefix + setup_file, "w")
        f.write( setup_template.format(hostname, "", "", username) )
        f.close()
    except Exception as e:
        print(" [ err ] cannot write {} file".format(setup_file) )
        print(e)
        f.close()

    print("end of new setup")





##  EXE ---------------------------------------------------

# setup routine:
#  - take as input a setup.hermes file
#  - create the configuration root directory
def setup(path = None) -> None:

    global setup_file, settings_file, auth_file
    
    print(" >> Welcome to Hermes setup wizard\n")
    
    
    
    
    ##  0)  sorting out things!
    
    # if path is not prompted, use current working dir
    if path is None:
        PREFIX = os.getcwd()
        print('using current pwd')
    else:  PREFIX = path
    
    
    # check for final /
    if(PREFIX[-1] != '/'):  PREFIX = PREFIX + '/'
    print('prefix :', PREFIX)
    
    
    # check if setup file exists (create template if does not exist)
    if not os.path.exists(PREFIX + setup_file):
        print(" [ war ] there is no setup file, creating one..." )
        print("   >>  {}".format(PREFIX + setup_file) )
        new_setup()
        sys.exit(1)
    
    # check if dir is empty (I suggest it to be empty!)
    if len(os.listdir(PREFIX) ) > 1:
        print("\n [ war ] target directory is NOT empty.\n Continue anyway?", end='')
        ans = input(" [Yy] > ") 
        if ans.lower() != "y": sys.exit(0) 

    
    
    ##  1)  setup file
    
    # read ...
    try:
        with open(PREFIX + setup_file, 'r') as f:  setup_file = f.read()
    except Exception as e:
        print(" [ err ] cannot read {} file".format(setup_file) )
        print(e)
        sys.exit(1)
    
    # ... & parse
    try:
        config = configparser.ConfigParser(allow_no_value=False)
        config.read_string("[setup]\n"+setup_file)  # manually fix missing section header
        this_settings = dict(config['setup'])
    except Exception as e:
        print(" [ err ] settings parse >> ", e )
        sys.exit(1)
    
    
    ##  2)  checking args
    
    if 'userid' not in this_settings.keys():    # assign username as default
        this_settings['userid'] = getpass.getuser()
    
    if 'hostname' not in this_settings.keys():  # assign system hostname as default
        this_settings['hostname'] = socket.gethostname()
    
    if 'token' not in this_settings.keys():
        print(" [ err ] no token provided!")
        sys.exit(1)
    
    
    ##  3)  writing settings
    
    # creating settings file
    print('create', settings_file)
    try:
        f = open( PREFIX + settings_file, "w")
        f.write( settings_template.format( this_settings['hostname'], this_settings['token']) )
        f.close()
    except Exception as e:
        print(" [ err ] cannot write {} file".format(settings_file) )
        print(e)
        f.close()
    
    # creating auth file
    print('create', auth_file)
    try:
        f = open( PREFIX + auth_file, "w")
        f.write( auth_template )
        if 'chatid' in this_settings.keys():
            user_str = this_settings['chatid'] + ',' + this_settings['userid'] + ',true,true'
            f.write( user_str )
        else:
            print(' [ info ] no authorized user, you can manually add them to', auth_file)
        f.close()
        
    except Exception as e:
        print(" [ err ] cannot write {} file".format(auth_file) )
        print(e)
        f.close()
        
    # creating external
    print('create', ext_file)
    try:
        f = open( PREFIX + ext_file, "w")
        f.write( external_template )
        f.close()
        
    except Exception as e:
        print(" [ err ] cannot write {} file".format(ext_file) )
        print(e)
        f.close()
    
    print("done!")
    
    

if __name__ == "__main__":
    print("Don't run this, fool of a Took!\n Look at README instead!")
    sys.exit(1)

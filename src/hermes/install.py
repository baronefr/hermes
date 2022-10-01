
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
log_dir = hermes.common.namespace['LOG_DIR']


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
"""

auth_template = "chatid,name,bonjour,active"




##  EXE ---------------------------------------------------


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






# setup routine:
#  - take as input a setup.hermes file
#  - create the settings root
def setup(path = None) -> None:

    global setup_file
    
    print(" >> Welcome to Hermes setup wizard\n")
    
    # if path is not prompted, use current working dir
    if path is None:
        PREFIX = os.getcwd()
        print('using current pwd')
    else:  PREFIX = path
    
    
    # check for final /
    if(PREFIX[-1] != '/'):  PREFIX = PREFIX + '/'
    print('prefix :', PREFIX)
    
    # TODO check if dir is empty
    
    
    # check if setup file exists (create template if does not exist)
    if not os.path.exists(PREFIX + setup_file):
        print(" [ war ] there is no setup file, creating one..." )
        print("   >>  {}".format(PREFIX + setup_file) )
        new_setup()
        sys.exit(1)
    
    
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
    
    
    
    ##  2)  check args
    do_auth = False
    
    
    
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
        f.write(  )
        f.close()
    except Exception as e:
        print(" [ err ] cannot write {} file".format(auth_file) )
        print(e)
        f.close()
    
    print("done!")

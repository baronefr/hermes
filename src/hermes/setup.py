
#########################################################
#   HERMES - telegram bot for messages & system control
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 30 Aug 2023
#--------------------------------------------------------

import os
import sys
import socket
import click
import subprocess
import shutil

import argparse
import configparser

from hermes import env_key
from hermes.common import namespace
from hermes.common import hprint

from hermes.templates import *


# ---------------------
#  some useful things
# ---------------------

def make_empty_setup(fname):
    """Create an empty setup file for Hermes, to be edited by the user before running setup script."""

    hprint.info("creating empty configuration file ({})".format(fname), color='blue')
    
    try:
        # get user details
        hostname = socket.gethostname()
        username = os.environ.get('USER')

        if hostname is None:  hostname = 'noname'
        if username is None:  username = 'nouser'

        assert isinstance(hostname, str), 'hostname must be a string'
        assert isinstance(username, str), 'username must be a string'

    except Exception as e:
        hprint.err("cannot retrieve current session env (hostname and username)")
        print(e)
        sys.exit(1)
    
    # print file for setup arguments
    try:
        f = open(fname, "w")
        f.write( setup_template.format(hostname, "", "", username) )
        f.close()
    except Exception as e:
        hprint.err("cannot write file {}".format(fname) )
        print(e)
        sys.exit(1)

    hprint.info("file written")

def make_settings(fname, setup) -> None:
    """Write the settings file in target directory."""

    # creating settings file
    try:
        f = open(fname, "w")
        f.write( settings_template.format( setup['hostname'], setup['token']) )
        f.close()
    except Exception as e:
        hprint.err("cannot write {} file".format(fname) )
        print(e)
        sys.exit(1)

def make_auth(fname, setup) -> None:
    """Write the user table file in target directory."""

    try:
        f = open(fname, "w")
        f.write( auth_template )
        if 'chatid' in setup.keys():
            user_str = setup['chatid'] + ',' + setup['userid'] + ',true,true'
            # remark: default settings are true and true
            f.write( user_str )
        else:
            hprint.warn("no authorized user yet, but you can manually add them to {}".format(fname) )
        f.close()
    
    except Exception as e:
        hprint.err("cannot write {} file".format(fname) )
        print(e)
        sys.exit(1)

def make_extra(fname) -> None:
    """Write the external module template."""

    try:
        f = open( fname, "w")
        f.write( extra_template )
        f.close()
        
    except Exception as e:
        hprint.err("cannot write {} file".format(fname) )
        print(e)
        sys.exit(1)

def make_env_link(fname, to):
    f = open(fname, "a")
    f.write( env_template.format( env_key, to) )
    f.close()


def make_systemd_service(fname):

    # get user data
    username = os.environ.get('USER')

    # get the name of python executable
    query = subprocess.run(['which', 'python3'], stdout=subprocess.PIPE)
    python_exe = query.stdout.decode('utf-8').strip('\n')

    # get the path of hermes script (with --server execution flag)
    query = subprocess.run(['which', 'hermes'], stdout=subprocess.PIPE)
    bot_exe = query.stdout.decode('utf-8').strip('\n')
    bot_exe += ' --server'

    hprint.info( 'linking {} -> {}'.format(python_exe, bot_exe), color='blue' )

    f = open(fname, "w")
    f.write( systemd_template.format(
            # username and group
            username, username,
            # env variable
            "{}={}".format(env_key, os.environ.get(env_key)),
            # exec start
            "{} {}".format(python_exe, bot_exe)
        )
    )
    f.close()





# ---------------------
#         MAIN
# ---------------------


def main():
    print('>> hermes setup utility')

    #---------------------------------
    #              ARGS
    #---------------------------------

    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    # select a setup file
    parser.add_argument("--setup", "-s", type=str, default=namespace['SETUP_FILE'],
                                          help="setup file")

    # quick actions
    parser.add_argument("--make", "-m", action="store_true", help="create a template setup file")
    parser.add_argument("--systemd", "-d", action="store_true", help="create a systemd service with current configuration")

    # advanced options
    parser.add_argument("--to", "-t", type=str, default='local', help="where to create the setup files")
    parser.add_argument("--force", "-f", action="store_true", help="force the setup procedure")
    parser.add_argument("--env", "-e", type=str, default='.bashrc', help="target env file")

    # etc
    parser.add_argument("--verbose", "-v", action="store_true", help="print more details about setup")

    args = parser.parse_args()
    VERB : bool = args.verbose  # additional verbosity (true or false)

    if VERB: print(args)


    ##  PARSING ----------------------
    if args.to == 'home':
        # config folder: home of current user
        PREFIX = os.path.expanduser('~')
        if PREFIX[-1] != '/': PREFIX += '/'  # add a final / to path
        PREFIX += '.hermes/'
    
    elif args.to == 'local':
        # config folder: .local of current user
        PREFIX = os.path.expanduser('~')
        if PREFIX[-1] != '/': PREFIX += '/'  # add a final / to path
        PREFIX += '.local/hermes/'
    
    else:
        # config folder: use custom prefix
        PREFIX = args.to

    SETUP_FILE = args.setup
    FORCE = args.force

    #---------------------------------
    #          QUICK ACTIONS
    #---------------------------------

    if args.make:
        make_empty_setup(SETUP_FILE)
        sys.exit(0)

    if args.systemd:
        make_systemd_service('hermes.service')
        sys.exit(0)
    

    #---------------------------------
    #          ENV CHECKING
    #---------------------------------

    # check: env variable for Hermes setup
    ENV_ = os.environ.get(env_key)   # use it later


    # check: setup file exists
    if not os.path.exists(SETUP_FILE):
        hprint.err("setup file ({}) does not exist".format(SETUP_FILE) )
        print("   ->   To create an empty template, run     hermes-setup -m")
        sys.exit(1)

    # check: target directory exists
    hprint.info(" target dir = {}".format(PREFIX), color='blue')
    if os.path.exists(PREFIX):
        hprint.warn(" target directory already exists")

        if ENV_ is not None:
            hprint.warn("Hermes has already an active env variable")
            hprint.append('{} = {}'.format(env_key, ENV_) )
            print('  There might be a working installation of Hermes in your environment.')
        else:
            hprint.append(' but no env variable has been found')

        if not FORCE:
            action = click.confirm('Do you want to overwrite it?', default=False)
            if not action:
                print('exit from setup')
                sys.exit(0)
            del action
        else:
            hprint.append('forcing overwrite')
    


    #---------------------------------
    #     EXECUTING SETUP ROUTINE
    #---------------------------------


    ### read the setup file ----------
    try:
        with open(SETUP_FILE, 'r') as f:
            SETUP_FILE = f.read()
    except Exception as e:
        hprint.err("cannot read {} file".format(SETUP_FILE) )
        print(e)
        sys.exit(1)

    ### parse the setup file ---------
    try:
        setup_ = configparser.ConfigParser(allow_no_value=False)

        if "[setup]" not in SETUP_FILE:
            # fix missing section header
            SETUP_FILE = "[setup]\n"+SETUP_FILE

        setup_.read_string(SETUP_FILE)  
        this_setup = dict(setup_['setup'])

    except Exception as e:
        hprint.err("setup file parser >> {}".format(e))
        sys.exit(1)

    ### check setup content ----------
    if 'token' not in this_setup.keys():
        hprint.err("no token provided in setup file!")
        sys.exit(1)

    
    ### checkpoint -------------------
    hprint.info("checkpoint: setup file", color='green')
    if VERB: print('setup file =', this_setup )


    ### create the directory ---------
    if not os.path.exists(PREFIX):
        hprint.info("creating settings dir ({})".format(PREFIX), color='blue')

        try: os.makedirs(PREFIX)
        except Exception as e: hprint.err("error creating the settings dir:\n{}".format(e))

    ### check permission of directory 
    if os.access(PREFIX, os.W_OK):   hprint.info("dir permissions ok", color='blue')
    else:
        hprint.err("permission failure for settings dir ({})".format(PREFIX))
        sys.exit(1)

    ### write settings file
    make_settings(PREFIX + namespace['SETTINGS_FILE'], this_setup)
    hprint.info("checkpoint: settings file")

    ### write user table file
    make_auth(PREFIX + namespace['AUTH_FILE'], this_setup)
    hprint.info("checkpoint: users file")

    ### write extra modules file
    make_extra(PREFIX + namespace['ONESHOTS'])
    hprint.info("checkpoint: custom commands file")

    print("\nsetup completed\n")


    #---------------------------------
    #   CREATING ENV CONFIGURATION
    #---------------------------------

    ### breakpoint: ignore env variable creation
    if args.env in ['None', 'none']:
        hprint.info('no env setup has been requested' , color='green')
        print("please, add manually this variable to your environment:")
        print( "{}={}".format( env_key, PREFIX) )
        sys.exit(0)
        # ......... program should end here
    
    
    ### look for env file --------
    if args.env == '.bashrc':
        # default:  use a .bashrc file located in the user home
        ENV_TARGET = os.path.expanduser('~')
        if ENV_TARGET[-1] != '/': ENV_TARGET += '/'
        ENV_TARGET = ENV_TARGET + '.bashrc'
    elif args.env == '.profile':
        # use a .profile file located in the user home
        ENV_TARGET = os.path.expanduser('~')
        if ENV_TARGET[-1] != '/': ENV_TARGET += '/'
        ENV_TARGET = ENV_TARGET + '.profile'
    else:
        # use custom file taken from user
        ENV_TARGET = args.env

    hprint.info('linking env variable to {}'.format(ENV_TARGET))
    try:
        if os.path.isfile(ENV_TARGET):  # create a backup copy if file exists
            shutil.copy2(ENV_TARGET, ENV_TARGET + '.bak' )  

        make_env_link( ENV_TARGET, PREFIX)

    except e:
        hprint.err('cannot append value to env file')
        print(e)
        sys.exit(1)
    
    hprint.info('linking complete, refresh your shell')
    sys.exit(0)



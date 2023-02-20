
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 18 Feb 2022
#--------------------------------------------------------

import os
import sys
import socket
import click

import argparse
import configparser



from hermes import env_key
from hermes.common import hprint
from hermes.common import namespace


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


def make_env_link(fname, to):
    f = open(fname, "a")
    f.write( env_template.format( env_key, to) )
    f.close()
    



def main():
    print('>> hermes setup utility')

    #---------------------------------
    #              ARGS
    #---------------------------------

    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--setup", "-s", type=str, default=namespace['SETUP_FILE'],
                                          help="setup file")
    parser.add_argument("--to", "-t", type=str, default='home', help="destination of setup")
    parser.add_argument("--force", "-f", action="store_true", help="force the setup procedure")
    parser.add_argument("--make", "-m", action="store_true", help="create an empty setup file")
    parser.add_argument("--env", "-e", type=str, default='.bashrc', help="target env file")
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
        PREFIX += '.local/.hermes/'
    
    else:
        PREFIX = args.to

    SETUP_FILE = args.setup
    FORCE = args.force

    #---------------------------------
    #          QUICK ACTIONS
    #---------------------------------

    if args.make:
        make_empty_setup(SETUP_FILE)
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
        # TODO create backup copy of file
        #make_env_link( ENV_TARGET, PREFIX)         # TODO remove comment before publish
        pass
    except e:
        hprint.err('cannot append value to env file')
        print(e)
        sys.exit(1)
    
    hprint.info('linking complete, refresh your shell')
    sys.exit(0)
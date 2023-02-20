
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 18 Feb 2022
#--------------------------------------------------------

import os
import sys
import argparse
import subprocess

from hermes import env_key
from hermes.common import hprint
from hermes.common import namespace
from hermes.bot.linguist import cli as mcli

import hermes.bot as hbot

import threading
from multiprocessing import Process
import signal
from time import sleep

def ignore_sighup():
    signal.signal(signal.SIGHUP, signal.SIG_IGN)


def start_thread(func, name=None, args = []):
    """Utility to start a background thread."""
    threading.Thread(target=func, name=name, args=args, daemon=True).start()



crop_command_len = 2

def check_installation():
    # TODO
    pass


def my_function():
    # do some time-consuming work
    sleep(5)
    print('Done with function')

def execute_command(commands : list, hbot, users : list, msg : str = None) -> None:
    
    #proc = subprocess.Popen(
    #    commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    #    #preexec_fn=os.setpgrp
    #)
    

    #pid = str(proc.pid)
    #print( 'process ID:', pid )

    #proc.wait()
    sleep(2)
    #exit_code = proc.poll()
    #output, error = proc.communicate()

    for userid in users:
        hbot.bot.send_message( userid, 'okkk' )

    sys.exit(0)
    #sys.exit(exit_code)


def main():
    print('>> hermes CLI')

    #---------------------------------
    #              ARGS
    #---------------------------------

    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--msg", "-m", type=str, default=None, help="message to be sent by the bot")

    parser.add_argument("--exe", "-e", type=str, default=[], nargs=argparse.REMAINDER, help="command to execute")
    parser.add_argument("--background", "-b", action="store_true", help="execute command in background, if any")
    parser.add_argument("--notice", "-n", action="store_true", help="notice the command to be executed")

    parser.add_argument("--user", "-u", type=str, default='all', help="select users (if more than one, must be comma separated)") # TODO

    parser.add_argument("--server" , "-s", action="store_true", help="start bot server")
    parser.add_argument("--dry-run", "-d", action="store_true", help="start bot (oneshot mode)")
    parser.add_argument("--check", "-c", action="store_true", help="check installation status")
    parser.add_argument("--override", "-o", type=str, default=None, help="override environment link")

    parser.add_argument("--verbose", "-v", action="store_true", help="additional verbosity of cli interface")

    args = parser.parse_args()
    VERB : bool = args.verbose  # additional verbosity (true or false)

    if VERB: print(args)


    #---------------------------------
    #          ENV CHECKING
    #---------------------------------

    if args.override is None:  PREFIX = os.environ.get( env_key )
    else:                      PREFIX = args.override

    if PREFIX is None:
        hprint.err('cannot find your private Hermes environment')
        hprint.append('did you link an environment variable?')
        sys.exit(1)
    else:
        hprint.info( "settings path is <{}>".format(PREFIX), color='blue' )
    

    # validate PREFIX: existence
    if not os.path.exists( PREFIX ):
        hprint.err('target directory does not exist')
        sys.exit(1)
    
    # validate PREFIX: check permissions




    #---------------------------------
    #          QUICK ACTIONS
    #---------------------------------

    if args.check is True:
        check_installation()
        sys.exit(0)



    #---------------------------------
    #          EXE
    #---------------------------------

    # setup the bot
    if VERB:  hprint.info( "loading bot module", color='blue')
    hb = hbot( override = PREFIX )
    hprint.info( "checkpoint: bot module loaded", color='green')


    # run the bot server
    if args.server:
        try:   hb.run()
        except Exception as err:
            hprint.err('server has stopped')
            print(err)
            sys.exit(1)
        sys.exit(0)

    # run the bot server for a oneshot test (bonjour)
    if args.dry_run:
        try:   hb.run(dry_run = True)
        except Exception as err:
            hprint.err('dry run has failed')
            print(err)
            sys.exit(1)
        sys.exit(0)



    if VERB: hprint.info( "{} users detected".format(len(hb.auth_users)) , color='blue')

    USER_ID_LIST = []
    if args.user == 'all':
        # use all the authorized users
        USER_ID_LIST = list( hb.auth_users.values() )

    elif args.user in hb.auth_users:
        # prompted user is present in authorized users
        USER_ID_LIST.append( hb.auth_users[args.user] )

    elif ',' in args.user:
        # users are prompted with a comma separated list
        usr = args.user.strip().split(',')
        for uu in usr:
            if uu in hb.auth_users:
                USER_ID_LIST.append( hb.auth_users[uu] )
            else:
                hprint.err('unknown user id ({}) in list of users'.format(uu))
                sys.exit(1)

    elif args.user.isdigit():
        # try to get user with index number (int)
        try:   usr = int(args.user)
        except ValueError:
            hprint.err('cannot convert user digit string to int')
            sys.exit(1)
        
        if usr >= len(hb.auth_users):
            hprint.err('user number ({}) exceeds number of available ({}) users'.format(usr, len(hb.auth_users)))
            # remark: index numeration starts from zero
            sys.exit(1)
        else:
            # take number
            USER_ID_LIST.append( list(hb.auth_users.values())[usr] )
    
    else:
        hprint.err('unknown user id : {}'.format(args.user) )
        sys.exit(1)

    if VERB: hprint.info( "{} users selected".format(len(USER_ID_LIST)) , color='blue')
    
    # run a command and notify about the execution
    if args.exe:
        hprint.info("executing <{}>".format( ' '.join(args.exe) ) )

        if args.notice:
            # send a message before command execution
            if len(args.exe) > crop_command_len:
                notice = ' '.join(args.exe[:crop_command_len]) + ' ...'
            else:
                notice = ' '.join(args.exe)

            for userid in USER_ID_LIST:
                hb.bot.send_message( userid, mcli.notice.format(notice) )
        
        print('main PID', os.getpid())

        if args.background is False:
            execute_command(args.exe, hb, USER_ID_LIST)
        else:
            #start_thread( execute_command, args=[args.exe, hb, USER_ID_LIST] )
            pp = Process( target=execute_command, args=[args.exe, hb, USER_ID_LIST])#, daemon=False)
            pp.daemon = True
            pp.start()
            print('thread started', pp.pid)
            #sleep(5)
            #sys.exit(0)


    if args.msg is not None:
        for userid in USER_ID_LIST:
            hb.bot.send_message( userid, args.msg )
        sys.exit(0)
    
    # if you see this, it means the program has not stopped previously
    # (which is what I want to happen...)
    print('nothing to execute?')
    #sys.exit(0)
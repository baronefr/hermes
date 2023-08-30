
#########################################################
#   HERMES - telegram bot for messages & system control
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 30 Aug 2023
#--------------------------------------------------------

import os
import sys
import argparse
import subprocess

from hermes import env_key, credits, version, status
from hermes.common import namespace
from hermes.common import hprint
from hermes.bot.linguist import cli as mcli

from hermes.bot.main import bot as hbot



###################
#  some settings  #
###################

# some useful properties
crop_command_len = 2   # max len of command to send in msg
addition_separator = "\n---\n"  # separator when appending output message




def hook_message(msg : str, hook : str) -> str:
    """
    Given a message msg, extracts all the lines which have a flag ``hook``.
    If `hook` is 'all', the full message is returned.
    """

    if hook == 'all': # return the full message
        return msg
    else:
        msg = msg.splitlines()
        out = []
        for mm in msg: 
            if hook in mm: out.append(mm.strip(hook))
        out = '\n'.join(out)
    
    return out



def execute_command(commands : list, hbot, users : list, msg : str = None, spawn_message = True, hook = None) -> int:
    """Execute a command in a child process and send a message about its exit status."""

    proc = subprocess.Popen(
        commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )

    msg = '' if msg is None else '({})'.format(msg)

    if spawn_message:
        # send a message before command execution
        if len(commands) > crop_command_len:
            notice = ' '.join(commands[:crop_command_len]) + ' ...'
        else:
            notice = ' '.join(commands)

        for userid in users:
            hbot.bot.send_message( userid, mcli.notice.format(notice) )

    pid = str(proc.pid)
    hprint.info("command PID : {}".format(pid), color='blue' )

    # wait for process
    proc.wait()
    exit_code = proc.poll()
    output, error = proc.communicate()

    # handle process output
    if exit_code == 0:
        hprint.info('process exit without error')
        stat = mcli.exe_ok.format(msg)
        addition = hook_message(output, hook)
    else:
        hprint.err('process exit with error ({})'.format(exit_code) )
        hprint.append(error)
        stat = mcli.exe_error.format(msg, exit_code)
        addition = error  # append error to message

    addition = '' if addition == '' else addition_separator+addition

    # send message to the users
    for userid in users:
        hbot.bot.send_message( userid, stat + addition )

    sys.exit(exit_code) # returns exit code of child process




###################
#       CLI       #
###################

def main():
    """
    Hermes command line interface.
    """

    print('>> hermes CLI')

    #---------------------------------
    #              ARGS
    #---------------------------------

    parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    # just send a message
    parser.add_argument("--msg", "-m", type=str, default=None, help="message to be sent by the bot")
    parser.add_argument("--image", "-i", type=str, default=None, help="attach an image")
    parser.add_argument("--file", "-f", type=str, default=None, help="attach a generic file")

    # execute something and send a message when execution is completed
    parser.add_argument("--exe", "-e", type=str, default=[], nargs=argparse.REMAINDER, help="command to execute")
    parser.add_argument("--background", "-b", action="store_true", help="execute command in background, if any (experimental)")
    parser.add_argument("--notice", "-n", action="store_true", help="notice the command to be executed")
    parser.add_argument("--hook", "-k", type=str, default=namespace['CLI_HOOK'], help="placeholder string to hook from exe output")

    # bot execution
    parser.add_argument("--server" , "-s", action="store_true", help="start bot server")
    parser.add_argument("--dry-run", "-d", action="store_true", help="start bot (oneshot mode)")
    
    # select users to whom the message will be sent
    parser.add_argument("--user", "-u", type=str, default='all', help="select users (if more than one, must be comma separated)")

    # informative commands
    parser.add_argument("--list-users", "-l", action="store_true", help="list available users")
    parser.add_argument("--check", "-c", action="store_true", help="check installation status")
    #parser.add_argument("--tasks", "-t", action="store_true", help="list tasks")       # TODO in next release

    # advanced options
    parser.add_argument("--override", "-o", type=str, default=None, help="override environment link")
    parser.add_argument("--verbose", "-v", action="store_true", help="additional verbosity of cli interface")

    # etc
    parser.add_argument("--about", "-a", action="store_true", help="about the author of this bot")

    args = parser.parse_args()
    VERB : bool = args.verbose  # additional verbosity (true or false)

    if VERB: print('cli args :', args)


    if args.about:  # print the credits message
        version()
        credits()
        sys.exit(0)

    if args.check:
        status()
        sys.exit(0)
    
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
        if VERB: hprint.info( "settings path is <{}>".format(PREFIX), color='blue' )
    

    # validate PREFIX: existence
    if not os.path.exists( PREFIX ):
        hprint.err(f'target directory ({PREFIX}) does not exist')
        sys.exit(1)
    
    # validate PREFIX: check permissions 
    #  TODO




    #---------------------------------
    #          QUICK ACTIONS
    #---------------------------------

    # pass



    #---------------------------------
    #          EXE
    #---------------------------------

    # setup the bot
    if VERB:  hprint.info( "loading bot module", color='blue')
    hb = hbot( override = PREFIX, external = False )
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


    # just list available users
    if args.list_users:
        hprint.info( "listing available users:", color='blue')
        print('-'*30)

        i = 0
        for k, v in hb.auth_users.items():
            hidden = str(v)[:4] + '*'*len(str(v)[4:])
            print( '  {}) '.format(i), k, hidden)
        
        print('-'*30)
        sys.exit(0)





    if VERB: hprint.info( "{} users detected".format(len(hb.auth_users)) , color='blue')

    # select users depending on user arg ---------------
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
    


    # run a command and notify after its execution
    if args.exe:
        hprint.info("executing <{}>".format( ' '.join(args.exe) ), color = 'blue' )

        # setup the output text hook flag
        HOOK = args.hook
        if HOOK in ['None','none']:  HOOK = None

        if args.background is False:
            execute_command(args.exe, hb, USER_ID_LIST, spawn_message = args.notice, msg=args.msg, hook = HOOK)
        else:
            # note: this should work only on UNIX-like systems
            pid = os.fork()
            if pid == 0:
                os.setsid()  # creates a new session
                if VERB: hprint.info("continue on detached process {}".format( os.getpid() ) )
                execute_command(args.exe, hb, USER_ID_LIST, spawn_message = args.notice, msg=args.msg, hook = HOOK)
            else:
                # exit from foreground execution
                if VERB: print('Hermes main PID [{}]'.format(os.getpid()) )
                sys.exit(0)


    # just send an image
    if args.image is not None:

        try:    photo = open(args.image, 'rb')
        except:
            hprint.err( 'cannot open image file {}'.format(args.image) )
            sys.exit(1)

        for userid in USER_ID_LIST:
            hb.bot.send_photo( userid, photo, caption = args.msg )
        if VERB: hprint.info("image sent" )
        sys.exit(0)



    # just send a file
    if args.file:

        try:    doc = open(args.file, 'rb')
        except:
            hprint.err( 'cannot open doc file {}'.format(args.file) )
            sys.exit(1)

        for userid in USER_ID_LIST:
            hb.bot.send_document( userid, doc, caption = args.msg )
        if VERB: hprint.info("document sent" )
        sys.exit(0)



    # just send a txt message
    if args.msg is not None:
        for userid in USER_ID_LIST:
            hb.bot.send_message( userid, args.msg )
        if VERB: hprint.info("message sent" )
        sys.exit(0)



    # if you see this, it means the program has not stopped previously
    #  (which is exactly what I want to happen...)
    hprint.warn('nothing to execute?')
    sys.exit(0)

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 27 july 2022
#--------------------------------------------------------

#  This class is the BOT logger.
#   DO NOT EDIT!

import os
from datetime import datetime
import stat

from hermes.common import *

###############
#  LOG files  #
###############

# log files placeholders (DO NOT CHANGE...)
UNAUTH_LOG = hermes.common.namespace['BLOG_UNAUTH']       # log of all unauthorized users
AUTH_USER_LOG = hermes.common.namespace['BLOG_AUTH_USER'] # a log for each authorized user
REGISTER_PIPE = hermes.common.namespace['BLOG_REGISTER']   # a log for users which require registration

# log file headers
BOT_LOG_HEADER = hermes.common.namespace['BLOG_HEAD']

# timestamp to use in log files
TIME_FORMAT = hermes.common.namespace['LOG_TIMESTAMP']

# header of the message to be logged
#    default:     [current time] ...
def entry_head():
    now = datetime.now()
    return "[{}] ".format( now.strftime(TIME_FORMAT) )





#  LOGGER CLASS -------------------------------------------------
#
#  This class handles the logging for Hermes Bot.
#
class botlogger():
    
    def __init__(self, path, autocreate = True) -> None:
    
        now = datetime.now()
        self.path = path
        
        # check path existence
        if not os.path.exists(self.path):
            if autocreate:   os.mkdir(self.path)
            else:   raise Exception("log dir does not exist, autocreate is disabled")
        
        # create unauth log file
        if autocreate:
            if not os.path.exists(self.path + UNAUTH_LOG):
                with open(self.path + UNAUTH_LOG, 'w') as f:
                    f.write( BOT_LOG_HEADER.format('unauthorized users', now.strftime(TIME_FORMAT)) )
        
        # TODO  test if log files are writable
    
    
    ##################
    #  log functions #
    ##################
    
    # add a message to the NOT authorized users log
    def unauth(self, text : str, chatid : int) -> None:
        this_file = self.path + UNAUTH_LOG
        with open(this_file, "a") as this_log:
            this_log.write(entry_head() + f"[{chatid}] " + text + "\n")
    
    
    # add a message to the authorized user log
    def auth(self, text : str, chatid : int) -> None:
        this_file = self.path + AUTH_USER_LOG.format(str(chatid))
        with open(this_file, "a") as this_log:
            this_log.write(entry_head() + text + "\n")
    
    
    ##################
    # register funct #
    ##################
    
    # check if register is available
    #  Returns:    None  if it is not available
    #              str   (path to register) if available
    def check_register(self):
        this_pipe = self.path + REGISTER_PIPE
        
        # check if register is available
        #if stat.S_ISFIFO(os.stat(this_pipe).st_mode):
        if os.path.exists(this_pipe): return this_pipe
        else: return None


#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 27 july 2022
#--------------------------------------------------------

#  This class is the BOT logger.
#   DO NOT EDIT!

import os.path
from datetime import datetime



# default log file path (can be overridden by init arg)
LOG_PATH_DEFAULT = "./log"



###############
#  LOG files  #
###############

# log files placeholders
UNAUTH_LOG = "unauth.log"       # log of all unauthorized users
AUTH_USER_LOG = "user_{}.log"   # a log for each authorized user
REGISTER_LOG = "register.log"   # a log for users which require registration

# log file headers
log_header = "Hermes Telegram bot - log file [{}]\n init: {}\n============================\n\n"

# timestamp to use in log files
TIME_FORMAT = "%Y/%m/%d %H:%M:%S"

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
    
    def __init__(self, path = None, autocreate = True) -> None:
    
        now = datetime.now()
    
        if path is None: self.path = LOG_PATH_DEFAULT
        else: self.path = path
        
        if autocreate:
            # create the log files, if they don't exist       
            if not os.path.exists(self.path + UNAUTH_LOG):
                with open(self.path + UNAUTH_LOG, 'w') as f:
                    f.write( log_header.format('unauthorized users', now.strftime(TIME_FORMAT)) )
            
            # ...
            # TODO  create ALL log files
        
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
    
    # add the user id to the register queue to gain access
    def register(self, chatid) -> None:
        this_file = self.path + REGISTER_LOG
        with open(this_file, "a") as this_log:
            this_log.write(entry_head() + str(chatid) + "\n")

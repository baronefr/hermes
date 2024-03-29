
#########################################################
#   HERMES - telegram bot for messages & system control
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 27 Jul 2023
#--------------------------------------------------------

import telebot

import sys
import configparser
from configparser import ExtendedInterpolation
from datetime import datetime
from types import ModuleType
import io

from hermes.common import *
from hermes.task.logger import tasklogger
from hermes.task.logger import get_random_id

from hermes.task.linguist import std as mstd



#  utilities -------------------------------------------------------

#     print a time interval with a user-friendly format.
def compute_dt_readable(diff):
    
    days = diff.days
    hours,remainder = divmod(diff.seconds,3600)
    minutes,seconds = divmod(remainder,60)
    readable = []
    if days != 0:    readable.append(str(days)+'d')
    if hours != 0:   readable.append(str(hours)+'h')
    if minutes != 0: readable.append(str(minutes)+'m')
    readable.append(str(seconds)+'s')
    return ' '.join(readable)

#    a decorator to catch all the exceptions
#     -->  your code will continue in any case!
def failsafe(function):
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception as err:
            print(' [hermes] failsafe :', err, file = sys.stderr)
            if(err.__context__ != None):
                print(' | ', err.__context__, file = sys.stderr)
    return wrapper
    

# time format used to save an image, if other names are not provided
PICTURE_TIME_FORMAT = "_%H-%M-%S"
PICTURE_DEFAULT_EXT = '.png'




# ------------------------------------------------------------------
#  Task object -----------------------------------------------------
#
class task():
    
    @failsafe
    def __init__(self, settings = None, alias = None, user = 'default',
                 logless = False, allquiet = False) -> None:
        
        
        ##    housekeeping  -------------------------------
        
        # if argument is not valid, override settings dir with default policy rule
        if settings is None: PREFIX = hermes.common.settings_default_policy()
        else:                PREFIX = settings
        
        if PREFIX[-1] != '/': PREFIX = PREFIX + '/'   # be sure last char is /
        
        # manage args
        self.__allquiet = bool(allquiet)
                
        # locate & parse the settings file
        try:
            settings_file = PREFIX + hermes.common.namespace['SETTINGS_FILE']
            
            # read and parse configuration from file
            config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
            config.read(settings_file)
        except Exception as err:
            raise Exception('error in settings file IO') from err


        # get argument
        try:
            # bot
            MYTOKEN = str( config['general']['token'] )
            
            # Task
            TASKP = str( config['task']['task_path'] )
            USRDF = str( config['task']['default_user'] )
            
        except Exception as err:
            raise Exception('Error in settings argument parser. Maybe something is missing?') from err
        
        
        # setup logger (if not logless mode) & this task alias
        if logless is False:
            try:   self.log = tasklogger(path = TASKP, alias = alias)
            except Exception as err:
                raise Exception('error in logger setup') from err
                
            self.id = self.log.id  # task id is generated by the logger
        else:
            print('[task] logless mode')
            self.log = None   # run in logless mode (only send messages in bot)
            self.id = get_random_id()
        
        if alias is None: self.alias = self.id
        else: self.alias = alias
        
        # init the bot object
        try:   self.bot = telebot.TeleBot(MYTOKEN)
        except Exception as err:
            raise Exception('bot init error') from err
        
        # get the list of available users
        auth_users, _ = hermes.common.read_permissions(
           PREFIX + hermes.common.namespace['AUTH_FILE']
        )
        
        # user handler
        #  Remark:  self.users will be the lists of users to notify
        if(user == 'default'):  # use the settings file configuration
            try:
                if (USRDF == 'all'):
                    # take all the users available
                    self.users = list( auth_users.values() )
                elif USRDF.isdigit():
                    # taking the user given by int value
                    self.users = [ list(auth_users.values())[ int(USRDF) ] ]
                else:
                    # use the string value ...
                    self.users = list( auth_users[USRDF] )
                    
            except Exception as err:
                raise Exception('error in user handler (origin from settings file)') from err
                
        elif user is None:
            self.users = []   # execute without any user to notify
            
        elif isinstance(user, str):
            try:  self.users = list( auth_users[user] )
            except Exception as err:
                raise Exception('error in user handler (invalid username)') from err
        
        elif isinstance(user, list):
            self.users = user     # use the list provided in input
        
        else:
            raise Exception('error in user handler (undefined behaviour), err = ' + str(user) )
        
        # obj required by waypoints
        self.wpoint_count = 0
        self.wpoint_dtime = datetime.now()
        
        # notify task creation
        try: self.__notify( mstd.init.format(self.alias) )
        except Exception as err:
            raise Exception('internal notify error (creation msg)') from err
        
        print("[task] <{}> has been initialized [id:{}]".format(self.alias, self.id) )
    
    




    # send txt or image to each user
    #  Note: for INTERNAL use, FAILSAFE to be handled explicitly!
    #
    #  Args:   txt     the string to send
    #          imgb    binary obj of the image to send
    #          quiet   if True, the message is sent without notification
    #
    #  Remark: if both txt and imgb are provided, the txt is sent as a caption
    def __notify(self, txt = '', imgb = None, quiet = False) -> None:
    
        if self.__allquiet: quiet = True # override for soundless notifications
        
        for uid in self.users:
            if imgb is None: self.bot.send_message(uid, txt, disable_notification = quiet)
            else:
                if(txt == ''): self.bot.send_photo(uid, imgb, disable_notification = quiet)
                else:  self.bot.send_photo(uid, imgb, caption = txt, disable_notification = quiet)
    
    
    
    # for public use (i.e. with failsafe & task alias included in message)
    @failsafe
    def notify(self, txt = '', img = None, quiet = False) -> None:
    
        # if img is a string, open the file
        try:
            if isinstance(img, str): img = open(img,'rb')
        except Exception as err:
            raise Exception('cannot open img (filename from string)') from err
        
        # call the internal method
        self.__notify(txt = "[{}] ".format(self.alias) + txt, imgb = img, quiet = quiet)
    
    
    
    @failsafe
    def plotify(self, module : ModuleType,
                    txt = '', quiet = False,     # message arguments
                    keep = False, show = False,  # handler arguments
                    **kwargs) -> None:           # pass to module all other kwargs
        
        # check input module
        try:
            if isinstance(module, ModuleType):
                mname = module.__name__
            elif( str( type(module) ) == "<class 'matplotlib.figure.Figure'>" ):
                # fig works fine too
                mname = 'matplotlib.custom'
            else:
                print(str( type(module) ))
                raise Exception('undefined behaviour')
        except Exception as err:
            raise Exception('module check error') from err
        
        # get the name of the module
        
        
        # start a buffer
        buf = io.BytesIO()
        
        # handle the module
        if( mname == 'matplotlib.pyplot' or mname == 'matplotlib.custom'):
            # handle MATPLOTLIB
            try: module.savefig(buf, **kwargs)
            except Exception as err:
                buf.close()
                raise Exception('error in handling matplotlib object') from err
        
        # TODO: add support for other libraries
        #   just add other if(...) here!
        
        else:
            buf.close()
            raise Exception('this module is not supported')
        
        
        # rewind the buffer & send message
        buf.seek(0)
        self.__notify(txt = "[{}] ".format(self.alias) + txt, imgb = buf, quiet = quiet)
        
        # ? keep the picture
        buf.seek(0)
        if isinstance(keep, bool):
            if keep is True:
                fname = self.alias + datetime.now().strftime(PICTURE_TIME_FORMAT) + PICTURE_DEFAULT_EXT
                print('[task] writing picture to', fname)
                with open(fname, "wb") as f:
                    f.write( buf.getbuffer() )
        elif isinstance(keep, str):
            with open(keep, "wb") as f:
                f.write( buf.getbuffer() )
        
        # ? show the picture
        if show is True:
            if mname == 'matplotlib.pyplot': module.show()
        
        # close buffer
        buf.close()
        
    
    # waypoint logger
    @failsafe
    def waypoint(self, txt = None, timed = False, reset = False) -> None:
        
        # reset waypoint counter, if requested
        if reset: self.wpoint_count = 0
        
        # increment waypoint counter
        self.wpoint_count = self.wpoint_count + 1
        
        # take current datetime
        this_dtime = datetime.now()
        
        # register in this task log
        try:
            if self.log is not None:
                self.log.record( 'waypoint ' + str(self.wpoint_count) )
        except Exception as err:
            raise Exception('logger error (waypoint)') from err
        
        # getting message ready
        msg = mstd.waypoint.format(self.alias, self.wpoint_count)
        if txt is not None:
            msg += ' ' + txt
        if timed:
            msg += "\n + {}".format( compute_dt_readable(this_dtime-self.wpoint_dtime) )
            
        # send telegram notification
        try: self.__notify( msg )
        except Exception as err:
            raise Exception('internal notify error (waypoint)') from err
        
        # update timestamp of last waypoint
        self.wpoint_dtime = this_dtime
    
    
    # add an heartbeat in task log (with custom text)
    @failsafe
    def heartbeat(self, txt = '') -> None:
        if self.log is not None: self.log.record('heartbeat ' + str(txt) )
        
    
    # export the current task log in external file
    @failsafe
    def export(self, file = './this.task') -> None:
        if self.log is not None: self.log.export_private_log(dest = file)
    
    
    # close this task
    #
    #   Input:  fail (optional)
    #            - if is a string:  record an error message
    #            - any other case:  just mark the task as failed
    #
    @failsafe
    def close(self, fail = None):
        
        if fail is None:
            log = 'closed'
            msg = mstd.closed.format(self.alias)
        elif isinstance(fail, str):
            log = 'failed, err message will follow:\n\n' + fail
            msg = mstd.failed_msg.format(self.alias, fail)          
        else:
            log = 'failed'
            msg = mstd.failed.format(self.alias, fail)
        
        if self.log is not None:  
            self.log.record( log )
            
        self.__notify( msg )
        
        if self.log is not None: 
            self.log.index_update( {'status': 'closed' if fail is None else 'failed'} )
    
    
    
    #################
    #   interface   #
    #################
    
    # reset the waypoint counter
    @failsafe
    def wpclear(self) -> None:
        self.wpoint_count = 0
    
    # manually set allquiet mode
    @failsafe
    def set_allquiet(self, new : bool) -> None:
        self.__allquiet = new
    
    # tell if operating in logless mode
    @failsafe
    def is_logless(self) -> bool:
        if self.log is None: return True
        else:                return False
    
    # tell if allquiet mode is enabled
    @failsafe
    def is_allquiet(self) -> bool:
        if self.__allquiet: return True
        else:                return False
    
    # set the default time signature for plotify save (if no other name is provided)
    @failsafe
    def plotify_set_time_signature(self, new : str) -> None:
        PICTURE_TIME_FORMAT = new
    
    # set the default extension for plotify save
    @failsafe
    def plotify_set_ext(self, new : str) -> None:
        PICTURE_DEFAULT_EXT = new



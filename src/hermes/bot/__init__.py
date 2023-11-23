
#########################################################
#   HERMES - telegram bot for messages & system control
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 27 Jul 2022
#--------------------------------------------------------

#from hermes.bot.main import bot as bot



import telebot

import os
import sys
from datetime import datetime
import configparser
from configparser import ExtendedInterpolation
from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction, isclass

from typing import Union

from hermes.common import *

from hermes.bot.logger import botlogger
from hermes.bot.handlers import handlers
from hermes.bot.linguist import std as mstd



__null_strings = ['', '0', 'none']

def parse_extra_components(self, config, settings_file : str, PREFIX : str) -> None:
    """
    Process the configuration of user defined functions and modules, along with bonjur application.

    Args:
        config (_type_): _description_
        settings_file (str): _description_
        PREFIX (str): _description_
    """
    external_oneshot = None
    external_query = None

    if config.has_section('modules'):
        try:
            # external modules - oneshot commands
            
            if config.has_option('modules', 'oneshot'):
                tmp = str( config['modules']['oneshot'] ).lower()
                if tmp not in __null_strings:
                    external_oneshot = tmp.replace(" ", "")   # remove spaces
                    external_oneshot = external_oneshot.split(",")  # make list of modules
            
            # external modules - query commands
            if config.has_option('modules', 'query'):
                tmp = str( config['modules']['query'] )
                if tmp.lower() not in __null_strings:
                    external_query = tmp.replace(" ", "")       # remove spaces
                    external_query = external_query.split(",")      # make list of modules
                

        except Exception as e:
            hprint.err('settings parsing error (optional), check file syntax')
            print(' settings file :', settings_file)
            print(' parse error >> ', e)
            sys.exit(1)
    
    else:
        # the settings file has no modules field, ignore
        pass    
    

    ##    import extern modules  ----------------------
    self.ext_oneshot = {};       self.ext_query = {}; 
    self.bonjour_pointer = None

    #  -> import oneshots
    if (external_oneshot is not None):
        try:
            # the custom .py file to look into
            ext_exe = PREFIX + hermes.common.namespace['ONESHOTS']
            hprint.info('importing custom functions from {}'.format(ext_exe), color='blue' )

            self.ext_module = SourceFileLoader("external", ext_exe).load_module()
            tmponeshot = getmembers(self.ext_module, isfunction)   # get a list of  (name, function pointer)

        except Exception as e:
            hprint.err('external module error')
            print(' module file :', ext_exe)
            print(' error >> ', e)
            sys.exit(1)

        # selecting only the function listed in settings file
        for name, pointer in tmponeshot:
            if name in external_oneshot:
                if name == 'bonjour':
                    self.bonjour_pointer = pointer   # bonjour is handled separately
                else:
                    self.ext_oneshot[name] = pointer
            else:
                if name != 'bonjour': # avoid warning for bonjour
                    hprint.warn("external function \"{}\" is not listed in settings, skip".format(name) )
    

    #  -> import query classes
    if external_query is not None:

        for qname in external_query:

            try:
                # the custom .py file to look into
                ext_exe = PREFIX + qname + '.py'
                hprint.info('importing custom class from {}'.format(ext_exe), color='blue' )

                self.ext_module = SourceFileLoader("external", ext_exe).load_module()
                tmpquery = getmembers(self.ext_module, isclass)   # get a list of  (name, function pointer)

                            # selecting only the class listed in settings file
                for name, pointer in tmpquery:
                    if name in external_query:
                        self.ext_query[name] = pointer
                        continue
                    else:
                        hprint.warn("external class \"{}\" is not listed in settings, skip".format(name) )

            except Exception as e:
                hprint.err('external query module error')
                print(' module file :', ext_exe)
                print(' error (non-fatal) >> ', e)


    
    # if still empty, disable it!
    if not self.ext_oneshot:  self.ext_oneshot = None
    if not self.ext_query:    self.ext_query   = None





# ------------------------------------------------------------------
#  Bot object ------------------------------------------------------
#
class bot():
    
    def __init__(self, override : Union[None,str] = None, info : bool = False, extra : bool = True) -> None:
        """
        Initialize the hermes bot object.

        Args:
            override (Union[None,str], optional): If None, the default policy to find the settings folder is used. Otherwise, a string pointing to a setup folder is expected. Defaults to None.
            info (bool, optional): Print bot information when the object is initialized. Defaults to False.
            extra (bool, optional): Load user defined components. Defaults to True.
        """
        
        ##    housekeeping  -------------------------------
        
        # if argument is not valid, override settings dir with default policy rule
        if override is None: PREFIX = hermes.common.settings_default_policy()
        else:                PREFIX = override
        
        if PREFIX[-1] != '/': PREFIX = PREFIX + '/'   # be sure last char is /
        
        if not os.path.isdir(PREFIX):
            hprint.err('settings path does not exist or it is not accessible')
            hprint.append("target dir {}".format(PREFIX))
            sys.exit(1)
            
        settings_file = PREFIX + hermes.common.namespace['SETTINGS_FILE']
        if not os.path.isfile(settings_file):
            hprint.err('settings file does not exist or it is not accessible')
            hprint.append("settings file : {}".format(settings_file) )
            sys.exit(1)
        
        
        
        # --- parsing settings files ----------------------
        
        # read and parse settings file
        config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
        config.read(settings_file)
        
        ### mandatory arguments
        try:
            # general settings
            self.hostname = str( config['general']['hostname'] )
            MYTOKEN = str( config['general']['token'] )
            
            # bot > privacy settings
            self.unauthorized_ghosting = config.getboolean('bot','unauthorized_ghosting')
            #  ->    do not reply to unauthorized users
            self.unknown_command_ignore = config.getboolean('bot','unknown_command_ignore')
            #  ->    do not notify the user in case of mispelled command
            
            # task path
            self.task_path = str( config['task']['task_path'] )
            
        except Exception as e:
            hprint.err('settings parsing error, check file syntax')
            print(' settings file :', settings_file)
            print(' parse error >> ', e)
            sys.exit(1)
        

        ### processing optional arguments
        # 1) external components
        if extra:
            parse_extra_components(self, config, settings_file, PREFIX)
        else:
            self.ext_oneshot = None
            self.ext_query   = None
            self.bonjour_pointer = None

        # 2) authorized users file
        self.auth_users, self.extra_lists = hermes.common.read_permissions(
            PREFIX + hermes.common.namespace['AUTH_FILE']
        )
        
        
        ##    init companion modules  ----------------------------
        
        # init the bot & logger object
        try:   self.bot = telebot.TeleBot(MYTOKEN, parse_mode='Markdown')
        except Exception as e:
            hprint.err('bot init error');  print(e); 
            sys.exit(1)
        
        try:   self.log = botlogger(path = PREFIX + hermes.common.namespace['LOG_DIR'])
        except Exception as e:
            hprint.err('logger init error');  print(e); 
            sys.exit(1)
        
        
        # print info if requested
        if info:
            print(' [Hermes] config info:')
            print('hostname   >', self.hostname)
            print('bot token  >', MYTOKEN)
            print('# of users >', len(self.auth_users))
            print('')
    

    
    # start the bot
    def run(self, bonjour = True, dry_run = False, init_task : bool = True) -> None:
        
        # init the function handler class
        hf = handlers(self, oneshot = self.ext_oneshot, query = self.ext_query)
        
        ###############
        #   handler   #
        ###############
        
        self.bot.message_handler(commands=["help"])( hf.help )
        self.bot.message_handler(commands=["about"])( hf.about )
        self.bot.message_handler(commands=["toctoc"])( hf.toctoc )
        #self.bot.message_handler(commands=["register"])( hf.register )  # deprecated in (server) bot implementation since v2
        
        self.bot.message_handler(commands=["power"])( hf.query_power )
        self.bot.message_handler(commands=["tasks"])( hf.query_tasks )
        self.bot.message_handler(commands=["sentinel"])( hf.query_sentinel )
        
        # Note:  If you want to create new commands, this is the place to link them in the HARD way!
        #
        #        I suggest you create a new class, import the object and link them here,
        #        like I did with hermes/bot/handlers.py .
        #        Otherwise, you can add your functions to my handlers class itself.
        #
        #   Remark:   In either case, you have to add here the command:
        #
        #     self.bot.message_handler(commands=["YOURCOMMAND"])( FUNCTION_POINTER )
        #
        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ##   !!  do not add other commands below this line  !!
        
        # link external oneshots
        if self.ext_oneshot is not None:
            self.bot.message_handler(commands=list(self.ext_oneshot.keys()) )( hf.oneshot )
        
        # link external queries
        if self.ext_query is not None:
            self.bot.message_handler(commands=list(self.ext_query.keys()) )( hf.query )
        
        # query handler (default + external)
        self.bot.callback_query_handler(func=lambda c:True)( hf.handler_events )
        
        # this has to be placed as final entry, to handle unmatched commands
        self.bot.message_handler(func = lambda message: True)( hf.unmatched )
        

        # create an empty task index file
        if init_task:
            try:
                task_path = self.task_path
                hermes.common.index_access(task_path, task_path + hermes.common.namespace['TASK_INDEX'] , datetime.now().strftime( hermes.common.namespace['LOG_TIMESTAMP'] ) )
            except:
                hprint.err('cannot init task index, but this is not fatal...')


        ###############
        #   connect   #
        ###############
        
        # connect to telegram bot
        try: print("connected to @" + self.bot.get_me().username, "as", self.hostname)
        except Exception as err:
            sys.exit(f" [!] bot connection has failed!\n{err}")
        
        # send bonjour msg
        if bonjour:
            # handle bonjour routine, if defined
            if self.bonjour_pointer is not None: bjstr = self.bonjour_pointer()
            # send it
            for userid in self.extra_lists['bonjour']:
                self.bot.send_message(userid, mstd.bonjour.format(self.hostname) )
                if self.bonjour_pointer is not None: self.bot.send_message(userid, bjstr )
        
        # exit with no error if dry run
        if dry_run:
            print('end of dry run')
            sys.exit(0)
        
        # polling messages
        try: self.bot.infinity_polling()
        except Exception as err:
            print("ERR in infinity polling")
            print(err)
            sys.exit(1)

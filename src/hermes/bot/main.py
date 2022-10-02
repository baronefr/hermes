#!/usr/bin/env python3

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 02 october 2022
#--------------------------------------------------------

#  This file is the bot object implementation. Here you can:
#   - add new commands to the bot (but implement in another file, please...)

import telebot

import os
import sys
import configparser
from configparser import ExtendedInterpolation
from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction, isclass

from hermes.common import *

from hermes.bot.logger import botlogger
from hermes.bot.handlers import handlers
from hermes.bot.linguist import std as mstd



# ------------------------------------------------------------------
#  Bot object ------------------------------------------------------
#
class bot():
    
    def __init__(self, settings = None, info = False) -> None:
        
        ##    housekeeping  -------------------------------
        
        # if argument is not valid, override settings dir with default policy rule
        if settings is None: PREFIX = hermes.common.settings_default_policy()
        else:                PREFIX = settings
        
        if PREFIX[-1] != '/': PREFIX = PREFIX + '/'   # be sure last char is /
        
        if not os.path.isdir(PREFIX):
            print('ERROR: settings path does not exist or it is not accessible')
            print(' [i] target dir :', PREFIX)
            sys.exit(1)
            
        settings_file = PREFIX + hermes.common.namespace['SETTINGS_FILE']
        if not os.path.isfile(settings_file):
            print('ERROR: settings file does not exist or it is not accessible')
            print(' [i] settings   :', settings_file)
            sys.exit(1)
            
            
        
        ##    parsing  ------------------------------------
        
        # read and parse configuration from file
        config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
        config.read(settings_file)
        
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
            
            # external modules - oneshot commands
            external_oneshot = str( config['external']['oneshot'] )
            if external_oneshot.lower() in ['', '0', 'none']:   external_oneshot = None
            else:
                external_oneshot = external_oneshot.replace(" ", "")   # remove spaces
                external_oneshot = external_oneshot.split(",")  # make list of modules
            
            # external modules - query commands
            external_query = str( config['external']['query'] )
            if external_query.lower() in ['', '0', 'none']:     external_query = None
            else:
                external_query = external_query.replace(" ", "")       # remove spaces
                external_query = external_query.split(",")      # make list of modules
            
        
        except Exception as e:
            print('ERROR: settings.ini parsing error, check syntax')
            print(' [i] settings.ini file :', settings_file)
            print(' [i] parse error >> ', e)
            sys.exit(1)
        
        self.auth_users, self.extra_lists = hermes.common.read_permissions(
           PREFIX + hermes.common.namespace['AUTH_FILE']
        )
        
        
        
        
        ##    import extern modules  ----------------------
        self.ext_oneshot = {};       self.ext_query = {};
        self.bonjour_pointer = None
        
        
        if (external_oneshot is not None) or (external_query is not None):
        
            ext_exe = PREFIX + hermes.common.namespace['EXTERNAL_EXE']  # the custom .py file to look into
            print(' [i] importing externals from ', ext_exe)
            
            try:
                self.ext_module = SourceFileLoader("external", ext_exe).load_module()
                tmponeshot = getmembers(self.ext_module, isfunction)   # get a list of  (name, function pointer)
                tmpquery   = getmembers(self.ext_module, isclass)      # get a list of  (name, class)
                
            except Exception as e:
                print('ERROR: external module error')
                print(' [i] module file :', ext_exe)
                print(' [i] error >> ', e)
                sys.exit(1)
        
        #  -> select oneshots
        if (external_oneshot is not None):
            # selecting only the function listed in settings file
            for name, pointer in tmponeshot:
                if name in external_oneshot:
                    if name != 'bonjour':  self.ext_oneshot[name] = pointer
                    else: self.bonjour_pointer = pointer   # bonjour is handled separately
                    continue
                else:
                    print(" [i] external function \"{}\" is not listed in settings, skip".format(name) )
        
        #  -> select queries
        if (external_query is not None):
            # selecting only the function listed in settings file
            for name, pointer in tmpquery:
                if name in external_query:
                    self.ext_query[name] = pointer
                    continue
                else:
                    print(" [i] external class \"{}\" is not listed in settings, skip".format(name) )
        
        # if still empty, disable it!
        if not self.ext_oneshot:  self.ext_oneshot = None
        if not self.ext_query:    self.ext_query   = None
        
        
        
        
        ##    init components  ----------------------------
        
        # init the bot & logger object
        try:   self.bot = telebot.TeleBot(MYTOKEN, parse_mode='Markdown')
        except Exception as e:
            print('ERROR: bot init error');  print(e);
            sys.exit(1)
        
        try:   self.log = botlogger(path = PREFIX + hermes.common.namespace['LOG_DIR'])
        except Exception as e:
            print('ERROR: logger init error');  print(e);
            sys.exit(1)
            
        
        # print info if requested
        if info:
            print(' [Hermes] config info:')
            print('hostname   >', self.hostname)
            print('bot token  >', MYTOKEN)
            print('# of users >', len(self.auth_users))
            print('')
    



    
    # start the bot
    def run(self, bonjour = True, dry_run = False) -> None:
        
        # init the function handler class
        hf = handlers(self, oneshot = self.ext_oneshot, query = self.ext_query)
        
        ###############
        #   handler   #
        ###############
        
        self.bot.message_handler(commands=["help"])( hf.help )
        self.bot.message_handler(commands=["about"])( hf.about )
        self.bot.message_handler(commands=["toctoc"])( hf.toctoc )
        self.bot.message_handler(commands=["register"])( hf.register )
        
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


if __name__ == "__main__":
    print("Don't run this, fool of a Took!\n run start_bot.py instead!")
    sys.exit(1)

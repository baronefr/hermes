#!/usr/bin/env python3

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 27 july 2022
#--------------------------------------------------------

#  This file is the bot object implementation. Here you can:
#   - add new commands to the bot (but implement in another file, please...)

import telebot

import os
import sys
import configparser
from configparser import ExtendedInterpolation

from hermes.common import *

from hermes.bot.logger import botlogger
from hermes.bot.handlers import handlers
from hermes.bot.linguist import std as mstd


LOGDIR = hermes.common.namespace['LOG_DIR']   


# ------------------------------------------------------------------
#  Bot object ------------------------------------------------------
#
class bot():
    
    def __init__(self, settings = None, info = False) -> None:
        
        # if argument is not valid, override settings file with default policy
        if settings is None:  settings = hermes.common.settings_default_policy()
        if not os.path.isfile(settings):
            print('ERROR: settings.ini does not exist or it is not accessible')
            print(' [i] settings.ini file :', settings)
            sys.exit(1)
            
        # read and parse configuration from file
        config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
        config.read(settings)
        
        SETTINGS_PATH = os.path.dirname(settings)
        if(SETTINGS_PATH == ''): SETTINGS_PATH = '.'
        
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
            print('ERROR: settings.ini parsing error, check syntax')
            print(' [i] settings.ini file :', settings)
            print(' [i] parse error in value', e)
            sys.exit(1)
        
        self.auth_users, self.extra_lists = hermes.common.read_permissions(
           SETTINGS_PATH + '/' + hermes.common.namespace['AUTH_FILE']
        )
        
        # init the bot & logger object
        try:   self.bot = telebot.TeleBot(MYTOKEN, parse_mode='Markdown')
        except Exception as e:
            print('ERROR: bot init error')
            print(e)
            sys.exit(1)
        
        try:   self.log = botlogger(path = SETTINGS_PATH + '/' + LOGDIR)
        except Exception as e:
            print('ERROR: logger init error')
            print(e)
            sys.exit(1)
        
        # print info if requested
        if info:
            print(' [Hermes] config info')
            print('hostname   :', self.hostname)
            print('bot token  :', MYTOKEN)
            print('# of users :', len(self.auth_users))
            print('')
    
    
    
    # start the bot
    def run(self, bonjour = True, dry_run = False) -> None:
        
        hf = handlers(self)  # pass itself to handlers to init the object
        
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
        self.bot.message_handler(commands=["rgb"])( hf.query_rgb )
        
        # Note:  If you want to create new commands, this is the place to link them!
        #
        #        I suggest you create a new class, import the object and link them here,
        #        like I did with hermes/bot/handlers.py .
        #        Otherwise, you can add your functions to my handlers class itself.
        #
        #   Remark:   In either case, you have to add here the command:
        #
        #     self.bot.message_handler(commands=["YOURCOMMAND"])( FUNCTION_POINTER )
        #
        
        self.bot.callback_query_handler(func=lambda c:True)( hf.handler_events )
        
        # this has to be placed as final entry, to handle unmatched commands
        self.bot.message_handler(func = lambda message: True)( hf.unmatched )
        
        
        ###############
        #   connect   #
        ###############
        
        # connect to telegram bot
        try: print("connected to @" + self.bot.get_me().username)
        except Exception as err:
            sys.exit(f" [!] bot connection has failed!\n{err}")
        
        # send bonjour msg
        if bonjour:
            for userid in self.extra_lists['bonjour']:
                self.bot.send_message(userid, mstd.bonjour.format(self.hostname) )
        
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

#!/usr/bin/env python3

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 27 july 2022
#--------------------------------------------------------

#  This file is the bot object implementation. Here you can:
#   - add new commands to the bot

import telebot

import os
import sys
import configparser
from configparser import ExtendedInterpolation

from hermes.common import *

from hermes.bot.logger import botlogger
from hermes.bot.handlers import handlers
from hermes.bot.linguist import std as mstd


class bot():
    
    def __init__(self, settings = None) -> None:
        
        # if argument is not valid, override settings file with default policy
        if settings is None:  settings = hermes.common.settings_default_policy()
        
        # read and parse configuration from file
        config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
        config.read(settings)
        
        SETTINGS_PATH = os.path.dirname(settings)
        if(SETTINGS_PATH == ''): SETTINGS_PATH = '.'
        
        try:
            # general settings
            self.hostname = str( config['general']['hostname'] )
            MYTOKEN = str( config['general']['token'] )
            
            # bot
            LOGDIR = str( config['bot']['log_dir'] )
            
            # bot > privacy settings
            self.unauthorized_ghosting = config.getboolean('bot','unauthorized_ghosting')
            #  ->    do not reply to unauthorized users
            self.unknown_command_ignore = config.getboolean('bot','unknown_command_ignore')
            #  ->    do not notify the user in case of mispelled command
            
        except Exception as e:
            print('ERROR: config file parsing error')
            print(e)
            sys.exit(1)
        
        self.auth_users, self.extra_lists = hermes.common.read_permissions(
           SETTINGS_PATH + '/' + hermes.common.namespace['AUTH_FILE']
        )
        
        self.bot = telebot.TeleBot(MYTOKEN)
        self.log = botlogger(path = SETTINGS_PATH + '/' + LOGDIR)
        

    # start the bot
    def run(self, bonjour = True) -> None:
        
        hf = handlers(self)  # pass itself to handlers to init the object
        
        ###############
        #   handler   #
        ###############
        
        self.bot.message_handler(commands=["help"])( hf.help )
        self.bot.message_handler(commands=["about"])( hf.about )
        self.bot.message_handler(commands=["toctoc"])( hf.toctoc )
        self.bot.message_handler(commands=["register"])( hf.register )
        
        self.bot.message_handler(commands=["power"])( hf.query_power )
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
        try: print("Connected to @" + self.bot.get_me().username)
        except Exception as err:
            sys.exit(f"[!] bot connection has failed!\n{err}")
        
        # send bonjour msg
        if bonjour:
            for userid in self.extra_lists['bonjour']:
                self.bot.send_message(userid, mstd.bonjour.format(self.hostname) )
            
        # polling messages
        try: self.bot.infinity_polling()
        except Exception as err:
            print(err)
            sys.exit(1)


if __name__ == "__main__":
    print("Don't run this, fool of a Took!\n run start_bot.py instead!")
    sys.exit(1)

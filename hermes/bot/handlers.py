#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 26 july 2022
#--------------------------------------------------------

import telebot

# messages
from hermes.bot.linguist import std as mstd
from hermes.bot.linguist import power as mpow
from hermes.bot.linguist import openrgb as mrgb

# services
from hermes.bot.functions import power


# given a telebot message obj, returns the content and the chatid
def unpack_msg(message):
    # simple message...
    try: action, chatid = message.text, message.chat.id
    # ... or query
    except: action, chatid = message.data, message.from_user.id
        
    return action, chatid


class handlers():

    def __init__(self, root):
    
        # take what you need from the root bot class
        self.bot = root.bot
        self.log = root.log
        
        self.auth_users = root.auth_users
        self.hostname = root.hostname
        
        self.unauthorized_ghosting  = root.unauthorized_ghosting
        self.unknown_command_ignore = root.unknown_command_ignore


    ################
    #   security   #
    ################
    
    # check if user is authorized & log the message
    def ifauthorized(function):
        def wrapper(self, message):
            action, chatid = unpack_msg(message)
            
            ### check for permission ###
            
            # -> user is authorized, execute wrapped function
            if chatid in self.auth_users.values():
                self.log.auth( action, chatid )
                function(self, message)
            
            # -> user is NOT authorized   
            else:
                self.log.unauth( action, chatid )
                if not self.unauthorized_ghosting:
                    self.bot.reply_to(message, mstd.unauthorized)
            
        return wrapper
    
  
    
    ################
    #   commands   #
    ################
    
    # help command
    @ifauthorized
    def help(self, message):
        self.bot.reply_to(message, mstd.hello)
    
    # just a toctoc
    @ifauthorized
    def toctoc(self, message):
        self.bot.send_message(message.chat.id, mstd.toc)
    
    # about the author
    @ifauthorized
    def about(self, message):
        self.bot.reply_to(message, mstd.about)
    
    # register command
    def register(self, message):  # TODO
        self.log.register( chatid )
    
    # handle the ELSE case, when no other command is matched
    @ifauthorized
    def unmatched(self, message):
        chatid = message.chat.id
        if not self.unknown_command_ignore:
            self.bot.reply_to(message, mstd.unknown)
    
    ################
    #   queries    #
    ################
    
    # note: answers to markup will be handled by handler_events(callback)
    
    # power control
    @ifauthorized
    def query_power(self, message):
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton(text=mpow.action_poweroff, callback_data="POWER_OFF"),
            telebot.types.InlineKeyboardButton(text=mpow.action_reboot, callback_data="POWER_REBOOT"),
            telebot.types.InlineKeyboardButton(text=mpow.action_status, callback_data="POWER_STATUS"),
        )
        self.bot.send_message(message.chat.id, mpow.markup_title, reply_markup=markup)
    
    # rgb control
    @ifauthorized
    def query_rgb(self, message):
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton(text=mrgb.rgb_off, callback_data="RGB_OFF"),
            telebot.types.InlineKeyboardButton(text=mrgb.rgb_yell, callback_data="RGB_YELLOW"),
        )
        self.bot.send_message(message.chat.id, mrgb.markup_title, reply_markup=markup)
    
    
    # TODO:  tasks  &  service monitor
    @ifauthorized
    def query_tasks(self, message):
        pass
    
    
    ############
    #  events  #
    ############

    # event handler
    @ifauthorized
    def handler_events(self, callback):
        query, chatid = unpack_msg(callback)
        
        query_exit = None
        
        if "POWER_" in query:
            query_exit = SPOWER.handler(query)
        
        elif "RGB_" in query:
            pass
        

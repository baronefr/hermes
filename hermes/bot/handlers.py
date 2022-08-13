#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 13 august 2022
#--------------------------------------------------------

import telebot
import os

# messages
from hermes.bot.linguist import std as mstd
from hermes.bot.linguist import task as mtsk
from hermes.bot.linguist import power as mpow
from hermes.bot.linguist import openrgb as mrgb

# services
import hermes.bot.fpower as fpower

# common
from hermes.common import *


# given a telebot message obj, returns the content and the chatid
def unpack_msg(message):
    # simple message...
    try: action, chatid = message.text, message.chat.id
    # ... or query
    except: action, chatid = message.data, message.from_user.id
        
    return action, chatid
    
def markup_fix(msg : str) -> str:
    return msg.replace('[',"\[")


class handlers():

    def __init__(self, root):
    
        # take what you need from the root bot class
        self.bot = root.bot
        self.log = root.log
        
        self.auth_users = root.auth_users
        self.hostname = root.hostname
        
        self.unauthorized_ghosting  = root.unauthorized_ghosting
        self.unknown_command_ignore = root.unknown_command_ignore
        self.task_path = root.task_path

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
    
    # register the user
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
            telebot.types.InlineKeyboardButton(text=mpow.action_poweroff, callback_data=fpower.events[0] ),
            telebot.types.InlineKeyboardButton(text=mpow.action_reboot, callback_data=fpower.events[1] ),
            telebot.types.InlineKeyboardButton(text=mpow.action_status, callback_data=fpower.events[2] ),
        )
        #   Remark:  associate here markup text & callback string
        self.bot.send_message(message.chat.id, mpow.markup_title, reply_markup=markup)
    
    
    
    
    # tasks
    @ifauthorized
    def query_tasks(self, message):
        
        try:
            index_file = self.task_path + hermes.common.namespace['TASK_INDEX']
        
            # check index existence
            if os.path.isfile(index_file) is False:
                # reply
                self.bot.send_message(message.chat.id, mtsk.index_not_available)
                return 0
        
            # get tasks from index
            eid, cid, als = hermes.common.index_get_tasks( index_file )
        
            if(len(als) == 0):
                # reply
                self.bot.send_message(message.chat.id, mtsk.index_empty)
                return 0
        
            # compose message
            msg = mtsk.markup_header
            markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        
        
            # first the active tasks ...
            if(len(eid) > 0):
                msg += mtsk.head_active
                for taskid in eid:
                    alias = als[ str(taskid) ]
                    if( alias == str(taskid) ):  msg += "\n- {}".format( str(taskid) )
                    else:  msg += "\n- {} ({})".format( alias, str(taskid) )
                    markup.add( telebot.types.InlineKeyboardButton(text=mtsk.markup_active + str(taskid), callback_data="TASKS_"+str(taskid)) )
                msg += '\n'
            
            # ... then closed tasks
            if(len(cid) > 0):
                msg += mtsk.head_closed
                for taskid in cid:
                    alias = als[ str(taskid) ]
                    if( alias == str(taskid) ):  msg += "\n- {}".format(  str(taskid) )
                    else:  msg += "\n- {} ({})".format( alias, str(taskid) )
                    markup.add( telebot.types.InlineKeyboardButton(text=mtsk.markup_closed + str(taskid), callback_data="TASKS_"+str(taskid)) )
                    
        except Exception as err:
            self.bot.send_message(message.chat.id, mtsk.task_query_error + err)
            return 0
        
        self.bot.send_message(message.chat.id, msg, reply_markup=markup)
    
    
    
    
    # sentinel   TODO
    @ifauthorized
    def query_sentinel(self, message):
        pass
    
    
    # rgb control   TODO
    @ifauthorized
    def query_rgb(self, message):
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            telebot.types.InlineKeyboardButton(text=mrgb.rgb_off, callback_data="RGB_OFF"),
            telebot.types.InlineKeyboardButton(text=mrgb.rgb_yell, callback_data="RGB_YELLOW"),
        )
        self.bot.send_message(message.chat.id, mrgb.markup_title, reply_markup=markup)
    
    
    ############
    #  events  #
    ############

    # event handler
    @ifauthorized
    def handler_events(self, callback):
    
        #get the query content and chatid
        query, chatid = unpack_msg(callback)
        
        
        # POWER MANAGER
        if   "POWER_" in query:
            # check if event is legal
            if query in fpower.events:
                self.bot.send_message(chatid, mstd.accepted_event.format( mpow.icon, query) , parse_mode='None')
                
                # these queries, if successful, admit no further reply ...
                if query == fpower.events[0]:     fpower.poweroff()
                elif query == fpower.events[1]:   fpower.reboot()
                
                # ... but this one will provide a reply
                elif query == fpower.events[2]:
                    rep = fpower.status()
                    self.bot.send_message(chatid, rep)
        
        
        
        # HERMES TASK: send the requested file log
        elif "TASKS_" in query:
        
            try:
                # get the task id & target task file name
                task_id = query.split("_", 1)[1]
                task_file = self.task_path + hermes.common.namespace['TASK_PRIVATE'].format(task_id)
            
            
                if os.path.isfile(task_file) is False:
                    self.bot.send_message(chatid, mtsk.task_file_error)
                    return 0
                    
                f = open(task_file, "r")
                msg = f.read()
                
                # fix Markdown parsing
                #msg = markup_fix(msg)
                
            except Exception as err:
                self.bot.send_message(chatid, mtsk.task_event_error + err)
                return 0
            
            # final reply
            self.bot.send_message(chatid, mtsk.task_message.format(task_id, msg), parse_mode='None')
        
        
        
        # TODO
        elif "SENTINEL_" in query:
            self.bot.send_message(chatid, mstd.unhandled_event)
        
        # TODO
        elif "RGB_" in query:
            self.bot.send_message(chatid, mstd.unhandled_event)
        

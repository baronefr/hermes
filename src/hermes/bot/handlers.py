
#########################################################
#   HERMES - telegram bot for messages & system control
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 13 Aug 2022
#--------------------------------------------------------

import telebot
from datetime import datetime

# messages
from hermes.bot.linguist import std as mstd
from hermes.bot.linguist import task as mtsk
from hermes.bot.linguist import power as mpow

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
    

# create help menu for external commands using docstrings
def make_help_external(eos = None, eqc= None) -> str:
    etc = ''
    if eos is not None:
        for command, pointer in eos.items():
            etc += str( mstd.help_external.format(command, pointer.__doc__) )
    if eqc is not None:
        for command, pointer in eqc.items():
            etc += str( mstd.help_external.format(command, pointer.__doc__) )
    return( ("  ---------\n" + etc) if etc != '' else '')


class handlers():

    def __init__(self, root, oneshot = {}, query = {}):
    
        # take what you need from the root bot class
        self.bot = root.bot
        self.log = root.log
        
        self.auth_users = root.auth_users
        self.hostname = root.hostname
        
        self.unauthorized_ghosting  = root.unauthorized_ghosting
        self.unknown_command_ignore = root.unknown_command_ignore
        self.task_path = root.task_path
        
        # link externals as dictionaries
        self.eos = oneshot;   self.eqc = query;



    ################
    #   security   #
    ################
    
    # check if user is authorized & log the message
    def ifauthorized(function):
        def wrapper(self, message):
            action, chatid = unpack_msg(message)
            
            # check timestamp of message
            try:
                in_time = abs(message.date - int(round(datetime.now().timestamp()))) < hermes.common.bot_timeout
            except Exception as err:
                in_time = True
            
            ### check for permission ###
                      
            # -> user is authorized, execute wrapped function
            if chatid in self.auth_users.values():
                self.log.auth( action + ('' if in_time else ' (retard)'), chatid )
                if in_time: function(self, message)
            
            # -> user is NOT authorized   
            else:
                self.log.unauth( action, chatid )
                if not self.unauthorized_ghosting:
                    self.bot.reply_to(message, mstd.unauthorized + ('' if in_time else ' (retard)') )
            
        return wrapper
    
    
    
    # register the user
    # DO NOT DECORATE WITH ifauthorized, need a special handle for this!
    def register(self, message):
        action, chatid = unpack_msg(message)
        
        if chatid in self.auth_users.values():
            # -> user is already authorized
            self.log.auth( action, chatid )
            #self.bot.reply_to(message, mstd.authorized )
            #return 0                                  TODO: ehm... revert! DEBUG 
        else:
            # -> if not authorized
            self.log.unauth( action, chatid )
            if not self.unauthorized_ghosting:
                self.bot.reply_to(message, mstd.unauthorized)
        
        try:
            # check if register is available
            #  -> this method returns a string with complete path
            check = self.log.check_register()
            if check is None:
                #print('[register] register is not open!')
                return 0
            
            # write to register
            with open(check, "a") as regist:
                regist.write( "{},{}\n".format(chatid, datetime.now().strftime("%Y/%m/%d_%H:%M:%S") ) )
            
            print('[register] completed')
            self.log.unauth('register completed', chatid)
            
        except Exception as err:
            print('[register] error:', err)
            
    
    ################
    #   commands   #
    ################
    
    # help command
    @ifauthorized
    def help(self, message):
        msg = mstd.help + make_help_external(self.eos, self.eqc)
        self.bot.reply_to(message, msg)
    
    # just a toctoc
    @ifauthorized
    def toctoc(self, message):
        self.bot.send_message(message.chat.id, mstd.toc)
    
    # about the author
    @ifauthorized
    def about(self, message):
        aboutme = """*HERMES* - Telegram Bot for system control and live code notifications.\nby Francesco Barone\nref: github.com/baronefr/hermes"""
        self.bot.reply_to(message, aboutme)
    
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
    
    
    ##############
    #  external  #
    ##############
    
    # handle external oneshot commands
    @ifauthorized
    def oneshot(self, message):
        action, _ = unpack_msg(message)
        self.bot.reply_to(message, self.eos[action[1:]]() )
    
    
    # handle external query commands
    @ifauthorized
    def query(self, message):
        # select the custom class, i.e.   target_class -> class head
        action, _ = unpack_msg(message)
        target_class = self.eqc[action[1:]]
        
        # create markup menu
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        for label, callback in target_class.menu:
            markup.add(
                        telebot.types.InlineKeyboardButton(text = label, 
                            callback_data = str(target_class.__name__ + '_' + callback) )
                      )
        
        # send message
        self.bot.send_message(message.chat.id, target_class.msg, reply_markup=markup)
    
    
    ############
    #  events  #
    ############

    # event handler
    @ifauthorized
    def handler_events(self, callback):
    
        # process message query
        query, chatid = unpack_msg(callback)
        key, action = query.split("_", maxsplit=1)
        
        # POWER MANAGER
        if key == "POWER":
            # check if event is legal
            if query in fpower.events:
                self.bot.send_message(chatid, mstd.accepted_event.format( mpow.icon, query) , parse_mode='None')
                
                # these queries, if successful, admit no further reply ...
                if query == fpower.events[0]:     fpower.poweroff()
                elif query == fpower.events[1]:   fpower.reboot()
                
                # ... but this one will provide a reply
                elif query == fpower.events[2]:
                    rep = fpower.status()
                    for msg in rep:
                        self.bot.send_message(chatid, msg.replace('_', '\_') )
        
        
        
        # HERMES TASK: send the requested file log
        elif key == "TASKS":
        
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
        
        
        
        # HERMES SENTINEL: TODO
        elif key == "SENTINEL":
            self.bot.send_message(chatid, mstd.unhandled_event)
        
        
        # manage user-defined query
        elif key in list(self.eqc.keys()):
            msg = self.eqc[key].event(action)
            if msg != '': self.bot.send_message(chatid, msg)
        
        else:
            # ignore wrong key queries
            pass


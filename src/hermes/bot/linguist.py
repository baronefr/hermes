
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 12 aug 2022
#--------------------------------------------------------

#  Default messages used by the bot. If you want to
# change the language of the messages, this is the right place!


class std:
    icon = "🖥️"
    
    #hello = "Hello there!"
    # bonjour message
    bonjour = icon + " *{}* is online"    # .format with hostname
    
    unauthorized = "⛔️ you are not authorized"
    authorized = "already authorized"
    unknown = "unknown command"
    toc = "I'm alive, thx"
    
    
    # help message, update with your commands
    help = """📢 Hello General Kenobi!\n
    /toctoc    bot check
    /about     dev credits
    /register  register new user
              
    /power     power management
    /tasks     Hermes Task
    /sentinel  process monitor"""
    
    help_external = "/{} - {}\n"
    
    unhandled_query = "unhandled query"
    unhandled_event = "unhandled event"
    
    accepted_event = "{} event {} accepted"  # arg: icon, event_name


class task:
    
    # header of the task index query
    markup_header = " TASKS ---------\n"
    
    # errors in query
    index_not_available = "⚠️ index file not available"
    index_empty = "⚠️ index is empty"
    task_query_error = "⭕️ task query error"
    
    # markup symbols
    head_active = '   *active*'
    markup_active = '▫️'
    head_closed = '\n   *closed*'
    markup_closed = '▪️'
    
    # errors in handler
    task_file_error = "⚠️ task file does not exist"
    task_event_error = "⭕️ task event error"
    
    # the task log
    task_message = "*TASK <{}>*  log\n--------\n{}\n--eof---"


class power:
    icon = "🔋"
    
    markup_title = icon + ' power options'
    
    action_poweroff = "🛑 poweroff"
    action_reboot = "🔆 reboot"
    action_status = "〽️ status"

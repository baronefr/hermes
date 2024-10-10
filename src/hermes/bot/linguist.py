
#########################################################
#   HERMES - github.com/baronefr/hermes
#--------------------------------------------------------

#  Default messages used by the bot. If you want to
# change the language of the messages, this is the right place!


class std:
    """Hermes Bot standard messages. English language."""

    icon = "🖥️"
    
    # bonjour message
    bonjour = icon + " *{}* is online"    # arg: hostname
    
    unauthorized = "⛔️ you are not authorized"
    authorized = "already authorized"
    unknown = "unknown command"
    toc = "I'm alive, thx"
    
    
    # help message, update with your commands
    help = """📢 Hello General Kenobi!\n
    /toctoc \tbot check
    /about  \tdev credits
              
    /power  \tpower management
    /tasks  \tHermes tasks
    """
    
    help_external_formatter = "    /{} \t {}\n"  # arg: commandname & description
    help_external_separator = "\n"
    
    unhandled_query = "unhandled query"
    unhandled_event = "unhandled event"
    
    accepted_event = "{} event {} accepted"  # arg: icon, event_name


class task:
    """Hermes Bot default messages for the Task integration. English language."""

    # header of the task index query
    markup_header = " TASKS ---------\n"
    
    # errors in query
    index_not_available = "⚠️ index file not available"
    index_empty = "🗑️ no tasks found, yet"
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
    """Hermes Bot default messages for the power management commands. English language."""
    
    icon = "🔋"
    
    markup_title = icon + ' power options'
    
    action_poweroff = "🛑 poweroff"
    action_reboot = "🔆 reboot"
    action_status = "〽️ status"


class cli:
    """Hermes Bot default messages for the CLI interface. English language."""

    notice = "\[cli] spawning cmd <{}>"
    exe_error = "\[cli] {} 🚫 cmd quitted (error {})"
    exe_ok = "\[cli] {} cmd ended ✅"

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 12 aug 2022
#--------------------------------------------------------

#  Default messages used by the bot. If you want to
# change the language of the messages, this is the right place!


class std:
    icon = "🖥️"
    
    hello = "Hello there!"
    bonjour = icon + " {} is online"  # .format with hostname
    
    unauthorized = "You are not authorized!"
    unknown = "Unknown command!"
    toc = "I'm alive, thx"
    
    help = 'Hello Kenobi!'
    
    about = " HERMES - ver 1.0 "
      
    
class power:
    icon = "🔋"
    
    markup_title = icon + ' power options'
    
    action_poweroff = "🔻 poweroff"
    action_reboot = "🔻 reboot"
    action_status = "🔻 status"


class openrgb:
    icon = "💡"
    
    markup_title = icon + ' rgb options'
    
    rgb_yell  = "🟡 yellow"
    rgb_dyell = "🟡 yellow dark"
    rgb_red   = "🔴 red"
    rgb_green = "🟢 green"
    rgb_blue  = "🔵 blue"
    rgb_off   = "⚫ off"

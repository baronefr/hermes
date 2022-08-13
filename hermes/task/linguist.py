
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 12 aug 2022
#--------------------------------------------------------

#  Default messages used by the Task framework. If you want to
# change the language of the messages, this is the right place!


class std:
    init = "✨ Task {} has spawned"
    
    waypoint = "[{}]\n waypoint #{}"
    
    failed = " Task {} has failed"
    failed_msg = failed + "\n err: [{}]"
    closed = " Task {} has been closed"

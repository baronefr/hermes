
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 12 aug 2022
#--------------------------------------------------------

#  This file contains the implementation of the system
#  functions that can be requested by the user.


class power():
    # Handle the power status of the machine.
    
    def __init__(self, bot):
        self.bot = bot
        
    def poweroff(self):
        pass
    
    def reboot(self):
        pass
        
    def status(self):
        pass
    
    def handler(self, query):
        print('handle POWER')
        
        if query == 'POWER_OFF':
            self.poweroff()
        elif query == 'POWER_REBOOT':
            self.reboot()
        elif query == 'POWER_STATUS':
            self.status()
            
        return query
        

class openrgb():
    # Handle the RGB lights of the machine.
    
    def __init__(self, bot):
        self.bot = bot
        
    def set_profile(self):
        pass
    
    def handler(self, query):
        print('handle RGB')
        pass

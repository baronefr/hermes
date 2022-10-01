#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 1 Oct 2022
#--------------------------------------------------------

__version__ = '0.1.0'
__major_review__ = '1 Oct 2022'


# system modules
import os

# my modules
import hermes
from hermes.bot  import bot
from hermes.task import task

from hermes.install import setup


###################
#  some settings  #
###################

# the environ variable name
env_key = 'HERMES_ENV_SETTINGS'


####################
#  easy interface  #
####################

# describe the HERMES status
def status():
    print(' installation path: ', os.path.dirname(hermes.__file__)) #abspath
    print('  environ key name: ', env_key)
    print(' this env variable: ', os.environ.get(env_key) )

def version():
    print('hermes | v', __version__)
    print(' major review:', __major_review__)

def credits():
    print('hermes | v', __version__)
    print(' F.P. Barone')
    print(' github.com/baronefr')
    

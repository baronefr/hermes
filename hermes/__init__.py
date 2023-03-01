#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 18 Feb 2023
#--------------------------------------------------------


# system modules
import os

# my modules
import hermes
from hermes.bot  import bot
from hermes.task import task
from hermes.version import __version__ as __version__
from hermes.version import __major_review__ as __major_review__

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
    print('ver : ', __version__, '(rev {})'.format(__major_review__) )

def credits():
    print('hermes | library for system control & notifications')
    print('')
    print(' ver : ', __version__, '(rev {})'.format(__major_review__) )
    print('')
    print(' dev: F.P. Barone - github.com/baronefr')
    

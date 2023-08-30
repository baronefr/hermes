
#########################################################
#   HERMES - telegram bot for messages & system control
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 30 Aug 2023
#--------------------------------------------------------


# system modules
import os

# my modules
import hermes
from hermes.version import __version__ as __version__
from hermes.version import __major_review__ as __major_review__


###################
#  some settings  #
###################

# define the environment variable that 
# points to settings folder path
env_key = 'HERMES_ENV_SETTINGS'


####################
#  easy interface  #
####################

# describe the HERMES status
def status():
    """Print main info about the current installation."""
    print(' installation path: ', os.path.dirname(hermes.__file__)) #abspath
    print('  environ key name: ', env_key)
    print(' this env variable: ', os.environ.get(env_key) )

def version():
    """Print current version."""
    print('ver : ', __version__, '(rev {})'.format(__major_review__) )

def credits():
    """Acknowledge the author. Thanks!"""
    print('hermes | library for system control & notifications')
    print('')
    print(' ver : ', __version__, '(rev {})'.format(__major_review__) )
    print('')
    print(' dev: F.P. Barone - github.com/baronefr')
    


#########################################################
#   HERMES - github.com/baronefr/hermes
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
    print('          ∟> ', os.environ.get(env_key) )

def version():
    """Print current version."""
    print('ver : ', __version__, '(rev {})'.format(__major_review__) )

def credits():
    """Acknowledge the author. Thanks!"""
    print('')
    print('hermes | Telegram bot for messages, task notifications & system management.')
    print(' ver : ', __version__, '(rev {})'.format(__major_review__) )
    print(' dev: F.P. Barone - github.com/baronefr')
    

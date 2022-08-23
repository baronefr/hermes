
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 12 August 2022
#--------------------------------------------------------

import os
import csv

import hermes

#  DEFAULT NAMESPACE -----------------------------------------------
#
#   My advice is to not change these options...
#
namespace = { # configuration files
              'SETTINGS_FILE'  : 'settings.ini',
              'AUTH_FILE'      : 'auth.txt',
              'LOG_DIR'        : 'log/',
              
              # bot log files
              'BLOG_UNAUTH'    : "unauth.log",       # log of all unauthorized users
              'BLOG_AUTH_USER' : "user_{}.log",      # a log for each authorized user
              'BLOG_REGISTER'  : "register.tmp",     # a register for user which ask for access
              
              # bot etc
              'BLOG_HEAD'      : "Hermes Telegram bot - log file [{}]\n init: {}\n============================\n\n",
              'LOG_TIMESTAMP'  : "%Y/%m/%d %H:%M:%S",
              
              # task files
              'TASK_INDEX'     : 'tasks.list',
              'TASK_PRIVATE'   : 'task_{}.log',
              
              # task etc
              'TINDEX_HEAD'    : "Hermes Task - index file [{}]\n",
              'TINDEX_FIELDS'  : "id,alias,pid,spawntime,status"
            }


#  SETTINGS POLICY -------------------------------------------------
#  
#  Each module (bot & task) has an optional argument 'settings'
#  of the init function, which overrides the following policy.
#  In priority order, the default policy hereby implemented is:
#    0) (override)
#    1) environment variable
#    2) current path of the executable
#
def settings_default_policy():
    # [1] environment variable
    settings = os.environ.get(hermes.env_key)
    
    # [2] local path
    if settings is None: settings = './' + namespace['SETTINGS_FILE']
    return settings




#  USER PERMISSIONS FILE -------------------------------------------
#  
#  This function reads the user permission file.
#
#  Returns:    - dictionary of (key : USER_NAME, CHAT_ID)
#              - dictionary of special lists (bonjour, ...)
#
def read_permissions(ufile):
    users_dict = {};  extra_dict = {};
    bonjour_list = []
    
    try:
        with open(ufile, mode='r') as auth_file:
            auth_csv = csv.DictReader(auth_file)
        
            # process each record
            for usr in auth_csv:
                # converting types & parsing boolean values
                usr['chatid'] = int(usr['chatid'])
                usr['active']  = True if usr['active']  in ['true', 'True'] else False
                usr['bonjour'] = True if usr['bonjour'] in ['true', 'True'] else False
        
                # skip users users marked as unactive
                if not usr['active']: continue
            
                # dispatch
                if usr['bonjour']: bonjour_list.append( usr['chatid'] )
                users_dict[ usr['name'] ] = usr['chatid']
                
    except Exception as err:
        raise Exception('cannot open auth file ' + ufile)
        
    extra_dict[ 'bonjour' ] = bonjour_list 
    return users_dict, extra_dict





#  INDEX checks -------------------------------------------------
#
def index_access(ipath, ifile, time = '', autocreate = True) -> None:

    # check the path
    if autocreate: os.makedirs(ipath, exist_ok=True)
    if os.path.exists(ipath) is False:
        if autocreate:
            raise Exception("[ERR] Task path does not exist and cannot be created.\n"
                    "Check if you have permission to create this folder.")
        else:
            raise Exception("[ERR] Task path does not exist, autocreate = False.")
    
    # create index, if not exist
    if os.path.isfile(ifile) is False:
        if autocreate:
            index_header = namespace['TINDEX_HEAD'] + namespace['TINDEX_FIELDS'] + '\n'
            with open(ifile, 'w') as f:
                f.write( index_header.format( time ) )
        else:
            raise Exception('[ERR] index does not exists, autocreate = False.')
    
    # check if index is writable
    with open(ifile, 'a') as f:
        if f.writable() is False:
            raise Exception('[ERR] index file is not writable')


def index_get_tasks(ifile : str):
    #  Arg:  ifile  name of auth file
    #
    #  Output:    - list of alive tasks (id)
    #             - list of closed tasks (id) (includes failed tasks)
    #             - dictionary with (key:id, alias)
    alive_tasks = [];
    closed_tasks = [];
    alias_tasks = {};
    
    with open(ifile, mode='r') as tindex:
        next(tindex) # skip header
        rtasks = csv.DictReader(tindex)
        for task in rtasks:
            if(task['status'] in ['failed','closed']): closed_tasks.append( task['id'] )
            else:                                      alive_tasks.append( task['id'] )
            alias_tasks[ str(task['id']) ] = str(task['alias'])
            
    return alive_tasks, closed_tasks, alias_tasks

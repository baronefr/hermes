
#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 12 August 2022
#--------------------------------------------------------

#  This class is the Task logger.
#   DO NOT EDIT!

import os
import secrets
import string
import csv
from datetime import datetime
import shutil


from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

from hermes.common import *



#  utilities & settings --------------------------------------------
#

# random name generator
RAND_ID_SIZE = 7    # size of the random id of the task, if no name is specified
def get_random_id():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(RAND_ID_SIZE))

# log files placeholders
TASK_IDX = hermes.common.namespace['TASK_INDEX']     # index of all tasks
TASK_LOG = hermes.common.namespace['TASK_PRIVATE']   # private log file for each task

# timestamp to use in task log files
TIME_FORMAT = hermes.common.namespace['LOG_TIMESTAMP']

# header of the message to be logged
#    default:     [current time] ...
def entry_head():
    now = datetime.now()
    return "[{}] ".format( now.strftime(TIME_FORMAT) )




#  INDEX EDIT METHODS -------------------------------------------------
#
#  These functions are used to edit the Task index.

def index_add(ifile : str, entries : dict) -> None:
    #       Add a new entry to the index file.
    #
    #     Arg:  - index file name
    #           - entries: dictionary with values to print
    #
    #  Remark:  the entries are ordered depending on TINDEX_FIELDS
    #
    to_print = []
    for field in hermes.common.namespace['TINDEX_FIELDS'].split(','):
        try:    to_print.append( str( entries[field] ) )
        except: to_print.append('-')
    with open(ifile, mode='a') as tindex:
        tindex.write(",".join(to_print) + "\n")

def index_touch(ifile: str, iid : str, new_entries : dict) -> None: # pattern, subst
    #       Update an entry in the index file
    #
    #     Arg:  - index file name
    #           - entries: dictionary with values to print
    #
    #  Remark:  the entries are ordered depending on TINDEX_FIELDS
    #
    
    # create temp file with updated row value
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(ifile) as old_file:
            for line in old_file:
                # change the correct row ...
                if( line.startswith(iid+',') ):
                    old_entries = list( line.split(',') )
                    to_print = []
                    for idx, field in enumerate(hermes.common.namespace['TINDEX_FIELDS'].split(',')):
                        try:    to_print.append( str( new_entries[field] ) )
                        except: to_print.append( old_entries[idx] )
                    new_line = ",".join(to_print) + "\n"
                    
                # ... do not touch the others
                else: new_line = line
                
                new_file.write(new_line) 
                
    # copy file permissions
    copymode(ifile, abs_path)
    
    # remove original file
    remove(ifile)
    
    # move new file
    move(abs_path, ifile)





#  LOGGER CLASS -------------------------------------------------
#
#  This class handles the logging for an hermes Task.
#  Remark:  all the errors have to be managed externally.
#
class tasklogger():
    
    def __init__(self, path = None, alias = None) -> None:
    
        # take the timing at function call
        now = datetime.now()
        
        # assign a random id (assume probabilities of conflict are null)
        self.id = get_random_id()
        
        if alias is None: alias = self.id
        
        # set target files (Task index & private log file)
        self.__task_idx = path + TASK_IDX
        self.__task_log = path + TASK_LOG.format( self.id )
        
        # check index access (create, if necessary)
        hermes.common.index_access(path, self.__task_idx, now.strftime(TIME_FORMAT) )
        
        # the properties to be written in index file (automatically ordered!)
        ee = { 'id' : self.id, 'alias' : alias,
               'pid' : os.getpid(), 'status' : 'created',
               'spawntime': now.strftime("%Y/%m/%d_%H:%M:%S") }
        
        # retrieve index entries ( executing, closed, dict of aliases )
        eid, _, als = hermes.common.index_get_tasks( self.__task_idx )
        
        # check if current alias is used in another active task
        if alias in [ als[key] for key in eid ]:
            print('WAR: alias already used by another task')
        
        # append new task to index
        index_add( self.__task_idx, ee)
        
        # creation in private log
        with open(self.__task_log, mode='w') as tlog:
            tlog.write(entry_head() + "created\n")
        
    
    #################
    # log functions #
    #################
    
    # export a copy of the private task log
    def export_private_log(self, dest : str) -> None:
        shutil.copyfile(self.__task_log, dest)
    
    # add a recond in task log
    def record(self, text : str) -> None:
        with open(self.__task_log, "a") as this_log:
            this_log.write(entry_head() + text + "\n")
    
    # update entry of an index file
    def index_update(self, new_values : dict) -> None:
        index_touch( self.__task_idx, self.id, new_values)

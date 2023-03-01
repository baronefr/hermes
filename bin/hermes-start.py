#!/usr/bin/env python3

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 26 July 2022
#--------------------------------------------------------


import hermes.bot as hbot
import sys

if __name__ == "__main__":

    # check for "--dry-run" flag
    argv = sys.argv[1:]
    if "--dry-run" in argv:  dry_run = True
    else:  dry_run = False
    
    # init the bot
    hb = hbot( info=dry_run )
    
    # run the bot
    hb.run( dry_run=dry_run)

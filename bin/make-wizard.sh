#!/bin/bash -e

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 2 Oct 2022
#--------------------------------------------------------

echo -e " >> Welcome to Hermes setup wizard\n"

HERMES_BASE="/opt/hermes"
USR_PRIVATE="/home/$USER/.local/hermes/"

pip3 install -e $HERMES_BASE/src/
mkdir -p $TARGET && cd "$_"

touch setup.hermes



# ...


setup-bot.py


cd
cp .bashrc .bashrc.bak
echo -e "# hermes env\nexport HERMES_ENV_SETTINGS=\"/home/$USER/.local/hermes/settings.ini\"" >> .bashrc
source .bashrc

#!/bin/bash -e

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 2 Oct 2022
#--------------------------------------------------------

echo -e " >> Welcome to Hermes setup wizard\n"

HERMES_BASE="/opt/hermes/"
USR_PRIVATE="/home/$USER/.local/hermes/"

echo "installation path  : $HERMES_BASE"
echo "configuration path : $USR_PRIVATE"
echo " ------------------:  you can change them inside the script"


##  routines ----------------------------------------------

function preliminaries() {
    pip3 install -e ${HERMES_BASE}src/
    mkdir -p $USR_PRIVATE && cd "$_"

    touch ${USR_PRIVATE}setup.hermes
    echo "done! now edit setup.hermes with your credentials"
}

function finalize() {
    cd $USR_PRIVATE
    ${HERMES_BASE}bin/setup-bot.py
    
    cd
    cp .bashrc .bashrc.bak
    echo -e "# hermes env\nexport HERMES_ENV_SETTINGS=\"${USR_PRIVATE}settings.ini\"" >> .bashrc
    source .bashrc
}

## --------------------------------------------------------


helpme() {
  printf "Usage: ..."
}

while getopts 'abf:v' flag; do
  case "${flag}" in
    i) preliminaries() ;;
    f) files="${OPTARG}" ;;
    v) verbose='true' ;;
    *) print_usage
       exit 1 ;;
  esac
done


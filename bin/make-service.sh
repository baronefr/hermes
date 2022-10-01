#!/bin/bash -e

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 1 Oct 2022
#--------------------------------------------------------

echo -e " >> Welcome to Hermes service wizard\n"



##  PRELIMINARIES -----------------------------------------

# retrieve username
echo "Your username is <$USER>"


# retrieve Hermes configuration path
if [[ -z "${HERMES_ENV_SETTINGS}" ]]; then
  echo "Hermes ENV variable is not defined! Exit (err)."
  exit 1
else
  TARGET_ENV="HERMES_ENV_SETTINGS=$HERMES_ENV_SETTINGS"
fi

# where to install the service file
TARGET="/etc/systemd/system/hermes.service"
echo "Target systemd service location is <$TARGET>"

# check if files exist (you must be in correct pwd)
TEMPLATE="./templates/hermes.service"
if [ -f "$TEMPLATE" ]; then
    echo ""
else 
    echo "Template service file does not exist. Are you sure that you are in  hermes/  main directory?"
    exit 1
fi

# wait for user
printf "%s" " [!] press any key to continue, Ctrl+C to abort"
read ans
echo
###################### wait for user ######################



##  EXECUTION ---------------------------------------------

# creating custom service file
tmpfile=$(mktemp)
echo "using tmp file $tmpfile"
cp $TEMPLATE $tmpfile

echo "replacing username"
sed -i "s/USERPLACEHOLDER/$USER/" $tmpfile

echo "replacing env variable"
TARGET_ENV_ESCAPED="${TARGET_ENV//\//\\\/}"  # escape the string... or sed won't work!
sed -i "s/ENVPLACEHOLDER/$TARGET_ENV_ESCAPED/g" $tmpfile


# root priviledge is required to install the service... so warn the user
echo -e "\n\n [!] warning: from now on, admin priviledges are required\n"


# copying tmp file to service location & removing tmp
sudo cp $tmpfile $TARGET
sudo rm $tmpfile

# enabling service for startup
sudo systemctl start hermes
sudo systemctl enable hermes

echo "done!"
exit 0

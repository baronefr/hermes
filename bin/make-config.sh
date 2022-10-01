#!/bin/bash -ei

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 1 Oct 2022
#--------------------------------------------------------

echo -e " >> Welcome to Hermes configuration wizard\n"



##  PRELIMINARIES -----------------------------------------

# retrieve username
echo "Your username is <$USER>"

# where to install the configuration file
TARGET="/home/$USER/.local/hermes/"                        # edit if you want to change it!
echo "Target configuration path is <$TARGET>"

# check if files exist (you must be in correct pwd)
if [ -f "./templates/settings.ini" ]; then
    echo ""
else 
    echo "Template file does not exist. Are you sure that you are in  hermes/  main directory?"
    exit 1
fi

# wait for user
printf "%s" " [!] press any key to continue, Ctrl+C to abort"
read ans
echo
###################### wait for user ######################



##  CONFIG ------------------------------------------------

echo -e "\n [i] In this section you have to prompt the requested fields. Hit Enter to confirm the value.\n"


while true; do
    # 1) ask for hostname (default: system hostname)
    echo -n -e "Insert Hermes hostname (if empty, default is $(hostname))\n > "
    read hermes_host
    if [[ "$hermes_host" == "" ]]; then
        hermes_host=$(hostname)
        echo "   using default value $hermes_host"
    fi
    
    # 2) ask for bot token (cannot be empty!)
    echo -n -e "Insert Telegram bot token (looks like 0123456789:abcdefghijklmnopqrstuvwxy_ABCDEFGHI)\n > "
    read hermes_token    
    
    # 3) ask for chat id (if empty, no user init!)
    echo -n -e "Insert your chatid (looks like 1234567890) (leave empty to skip)\n > "
    read hermes_chatid
    if [[ "$hermes_chatid" == "" ]]; then
        echo "   skip user add"
    fi
    
    # 4) if chatid is prompted, ask for userid (default: username)
    if [[ "$hermes_chatid" != "" ]]; then
        echo -n -e "Insert your userid (any spaceless string) (leave empty to use hostname itself)\n > "
        read hermes_userid
        if [[ "$hermes_userid" == "" ]]; then
            hermes_userid=$USER
            echo "   using default value $hermes_userid"
        fi
    fi
    
    #  eventually, ask to confirm the above data
    read -p " [!] Confirm the data above? [Yy] " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "\n***\n"
        break
    else
        echo -e "\n -> trying again...\n"
    fi
done




##  EXECUTION ---------------------------------------------

echo "spawning target directory"
mkdir -p $TARGET


echo "copying files"
cp templates/settings.ini $TARGET
cp templates/auth.txt $TARGET


echo "editing settings.ini"  # just replace the placeholder with prompted value
file="${TARGET}settings.ini"
sed -i "s/HOSTPLACE/$hermes_host/" $file
sed -i "s/TOKENPLACE/$hermes_token/" $file


if [[ "$hermes_chatid" != "" ]]; then
    echo "adding user to auth.txt"
    echo "$hermes_chatid,$hermes_userid,true,true" >> "${TARGET}auth.txt"
else
    echo "skipping new user append"
fi


# add env variable to bashrc
if [[ "$USER" != "root" ]]; then
    echo "append to bashrc"
    
    # make backup copy of bashrc
    cp /home/$USER/.bashrc /home/$USER/.bashrc.bak
    
    # edit bashrc
    echo -e "\n# hermes bot\nexport HERMES_ENV_SETTINGS=\"${TARGET}settings.ini\"\n" >> /home/$USER/.bashrc
    echo "sourcing new bashrc"
    export HERMES_ENV_SETTINGS="${TARGET}settings.ini"
else
    echo "user is root, skip bashrc sourcing"
fi


# dump the target path to file (required by service)
#echo "HERMES_ENV_SETTINGS=\"${TARGET}settings.ini\"" > config.hist


echo "done!"
exit 0

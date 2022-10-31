#!/bin/bash -e

#########################################################
#   HERMES - telegram bot for system control & notify
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  coder: Barone Francesco, last edit: 13 august 2022
#--------------------------------------------------------



#   SETUP -------------------------------------------------
#  getting ready for the registration procedure

# check Hermes env variable
if [[ -z "${HERMES_ENV_SETTINGS}" ]]; then
  echo 'hermes env is undefined!'
  exit 1
fi

# get the path of configuration files
TARGET="$(dirname "${HERMES_ENV_SETTINGS}")"
echo " [hermes] using config path $TARGET"

# set the names of register file
REGISTER_FILE="$TARGET/log/register.tmp"
AUTH_FILE="$TARGET/users.key"

# set time to wait for users to send the \register command
LINGER_TIME=10




#   OPENING REGISTER --------------------------------------
#  Users are required to send the Bot command  /register

# create the register
echo "creating the register $REGISTER_FILE"
touch $REGISTER_FILE

# wait for n seconds
echo -e "\n"
echo    " Now open the bot and send the command /register."
echo -e " This register will close in $LINGER_TIME seconds.\n"
sleep $LINGER_TIME
echo "register is closed"




#   PARSING REGISTER --------------------------------------
#  parse the values & remove the register file

# parse the register content
ic=0        # count entries
arrID=()    # store chatids
echo " -------------------------"
while read line; do
    # separate the arguments ( chatid , time signature )
    arrIN=(${line//,/ })
    
    echo " $ic ) id ${arrIN[0]}  at time  ${arrIN[1]}"
    arrID+=("${arrIN[0]}")
    ic=$((ic+1))
done < $REGISTER_FILE
echo " -------------------------"

echo "clearing the register"
rm $REGISTER_FILE
echo -e "\n\n"

# if register is empty
if (( ic == 0 )); then
  echo "No values found in register. Maybe there's something wrong with the bot?"
  exit 0
fi



#   SELECTING CHATID --------------------------------------
#  Choose among multiple chatids.

# if register has more values
if (( ic > 1 )); then
  echo "Choose which user you want to add. Ctrl+C to break."
  
  while :; do
    read -p " user [ 0 to $((ic-1)) ] > " number
  
    [[ $number =~ ^[0-9]+$ ]] || { echo "  [err] enter a number"; continue; }
    if ((number >= 0 && number < ic)); then
      hermes_chatid=${arrID[number]}
      break
    else
      echo "  [err] Selection out of range, try again. Ctrl+C to break."
    fi
  done

elif (( ic == 1)); then
  hermes_chatid=${arrID[0]}
fi

echo " candidate user is #$hermes_chatid."
echo -e "\n\n"




#   INPUT USERNAME ----------------------------------------
#  Users are required to insert a string alias for the chatid

# ask for nickname
while :; do
    read -p " Assign username (letters only) > " hermes_uname
    
    if [[ $hermes_uname =~ [^a-zA-Z] ]]; then
      echo "  [err] use only letters"; continue;
    else
      break
    fi
done

echo -e "\n\n"

#ask for bonjour
while true; do
  read -p " Do you wish to receive bonjour messages? > " hermes_bonj
  case $hermes_bonj in
        [Yy]* ) hermes_bonj=true;  break;;
        [Nn]* ) hermes_bonj=false; break;;
        * ) echo "Please answer yes or no.";;
  esac
done



#   RECORD NEW AUTH USER-----------------------------------
#

# formatting the new auth entry
hermes_new="$hermes_chatid,$hermes_uname,$hermes_bonj,true"

echo "Adding $hermes_new to auth file."
echo "You have 5 seconds to stop this program (Ctrl+C) and keep auth unchanged."
sleep 5

echo -n "writing to auth file ..."
echo "$hermes_new" >> $AUTH_FILE

echo " done"
exit 0

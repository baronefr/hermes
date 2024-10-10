#!/bin/bash

# --------------------------------------------
secs=$((5))
echo "waiting for $secs seconds"
while [ $secs -gt 0 ]; do
   echo -ne "$secs\033[0K\r"
   sleep 1
   : $((secs--))
done
# --------------------------------------------

echo "%HERMES% Hooked text number one"
echo "this text is not hooked"
echo "%HERMES% Hooked text number two"

sleep 1
exit 0
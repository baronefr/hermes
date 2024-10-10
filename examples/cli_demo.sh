#!/bin/bash

hermes -m 'spawning my shell script'

# --------------------------------------------
secs=$((5))
echo "waiting for $secs seconds"
while [ $secs -gt 0 ]; do
   echo -ne "$secs\033[0K\r"
   sleep 1
   : $((secs--))
done
# --------------------------------------------

hermes -m 'the script execution is completed'
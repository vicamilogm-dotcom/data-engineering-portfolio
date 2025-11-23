#!/usr/bin/env bash
connections=$(ss | grep "tcp.*ssh" | wc -l)
if [[ $connections > 0 ]]
then
    echo "Hey it looks like someone is connected"
else
    #poweroff
     echo "No hay conexiones SSH activas"
fi
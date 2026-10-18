#!/bin/bash

unclutter -idle 0 &
WATCH_DIR="/home/pi/drinksMachine"

while true; do
    black ~/drinksMachine >>  ~/drinksMachine/logs/output.log
    python3 ~/drinksMachine/main.py >> ~/drinksMachine/logs/output.log 2>&1 
    sleep 1
done


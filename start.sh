#!/usr/bin/env bash

if [ -s .running.pid ]; then
	echo "simulation server already running"
else
	nohup python sim_serv.py &
	echo $! > .running.pid
fi

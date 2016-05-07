#!/usr/bin/env bash

if [ -s .running.pid ]; then
	echo "simulation server already running"
else
	nohup python sim_serv.py &
	echo $! > .running.pid
	nohup mongod --dbpath $(pwd)/db &
	echo $! >> .running.pid
fi

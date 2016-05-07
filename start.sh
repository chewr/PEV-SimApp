#!/usr/bin/env bash

if [ -s .running.pid ]; then
	echo "simulation server already running"
else
	echo "Starting server..."
	nohup python sim_serv.py &
	echo $! > .running.pid
	echo "Starting mongod..."
	nohup mongod --dbpath $(pwd)/db &
	echo $! >> .running.pid
	echo "Started up!"
fi

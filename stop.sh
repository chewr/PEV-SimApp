#!/usr/bin/env bash

if [ -s .running.pid ]; then
	echo "stopping simulation server..."
	while read -r line
	do
		pid_to_kill="$line"
		echo "Killing $pid_to_kill"
		kill $pid_to_kill
	done < ".running.pid"
	## mv .running.pid pid_log.log
	rm .running.pid
	echo "done"
else
	echo "Sim server not running."
fi

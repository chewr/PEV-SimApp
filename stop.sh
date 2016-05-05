#!/usr/bin/env bash

if [ -s .running.pid ]; then
	echo "stopping simulation server..."
	while read -r line
	do
		name="$line"
		echo "Killing $name"
		kill $name
	done < ".running.pid"
	rm .running.pid
	echo "done"
else
	echo "Sim server not running."
fi

#!/usr/bin/env bash

cmd=`screen -ls | grep tmworkers | awk -F"." '{print $1}' | xargs`

if [ -z "$cmd" ]
	then
		echo "Loading tmworkers"
		screen -dmS tmworkers /home/dev/tm_workers/venv/bin/python3 /home/dev/tm_workers/manage.py runserver 127.0.0.1:8081
	else
		echo "Already started"
	fi


#!/usr/bin/bash

while true
do
	python3 photo-copy.py
	if [ $? -eq 0 ]
	then
		exit
	fi
	sleep 60
done

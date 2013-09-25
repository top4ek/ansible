#!/bin/bash

LOGROOT=~/SSHLogs
LOGDATE=$(date +%F)
LOGTIME=$(date +%H-%M-%S)

if [ "$#" == "0" ]; then
	ssh
else
    mkdir -p "${LOGROOT}/${LOGDATE}"
    ssh $* | tee -a "${LOGROOT}/${LOGDATE}/${LOGTIME}.log"
fi

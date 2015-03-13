#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

SITE_NAME="wakatime"
USER="nodraak"
GROUP="nodraak"

WORKINGDIR=/opt/$SITE_NAME-env/$SITE_NAME-site/

LOGFILE=$WORKINGDIR/../log/gunicorn.log
ERRFILE=$WORKINGDIR/../log/gunicorn_err.log
NUM_WORKERS=3 # how many worker processes : should be nb_cpu*2+1
USER=$USER
GROUP=$GROUP

cd $WORKINGDIR
source ../bin/activate
exec python main.py 2>> $ERRFILE


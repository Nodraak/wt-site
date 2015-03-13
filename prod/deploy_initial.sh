#!/bin/sh
# @Author: nodraak
# @Date:   2015-01-17 18:28:46
# @Last Modified by:   nodraak
# @Last Modified time: 2015-03-12 18:16:49

NAME="wakatime"
SITE_NAME="wakatime-site"
ENV_NAME="wakatime-env"
USER="nodraak"
GROUP="nodraak"
GIT_REPO="$SITE_NAME"
GIT_URL="https://github.com/Nodraak/$GIT_REPO"

set -e

# dependencies
echo "=> Dependencies ..."
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python2.7 python2.7-dev python-pip python-virtualenv python-software-properties  # 139 MB
sudo apt-get install nginx supervisor

# virtual env
echo "=> Virtual env ..."
cd /opt
sudo virtualenv $ENV_NAME
sudo chown -R $USER $ENV_NAME
sudo chgrp -R $GROUP $ENV_NAME
echo "=> Virtual env OK"

# git
echo "=> Git ..."
cd /opt/$ENV_NAME
mkdir log
git clone $GIT_URL

cd /opt/$ENV_NAME/$GIT_REPO
source ../bin/activate
pip install -r requirements.txt
echo "=> Git OK"

# nginx
echo "=> Nginx ..."
sudo cp prod/nginx-prod.conf /etc/nginx/sites-available/$NAME-prod

read -p "Customize /etc/nginx/sites-available/$NAME-* (do CTRL-Z, edit the file, then \fg)"

sudo ln -s /etc/nginx/sites-available/$NAME-prod /etc/nginx/sites-enabled/$SITE_NAME
sudo nginx -t
echo "=> Nginx OK"

# supervisor
echo "=> Supervisor"

cd /opt/$ENV_NAME/$GIT_REPO
sudo cp prod/supervisor.conf /etc/supervisor/conf.d/$NAME.conf

read -p "Customize /etc/supervisor/conf.d/$NAME.conf (do CTRL-Z, edit the file, then \fg)"

sudo supervisorctl reread
sudo supervisorctl reload
sudo supervisorctl start $NAME
echo "=> Supervisor OK"

echo "reloading all"
sudo service nginx restart
sudo service supervisor restart
sudo supervisorctl restart $NAME

echo "All done, no errors."

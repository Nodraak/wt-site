#!/bin/sh
# @Author: nodraak
# @Date:   2015-01-17 18:28:46
# @Last Modified by:   nodraak
# @Last Modified time: 2015-03-12 18:16:49

SITE_NAME="wakatime-site"
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
sudo virtualenv $SITE_NAME-env
sudo chown -R $USER $SITE_NAME-env/
sudo chgrp -R $GROUP $SITE_NAME-env/
echo "=> Virtual env OK"

# git
echo "=> Git ..."
cd /opt/$SITE_NAME-env
mkdir ../log

cd /opt/$SITE_NAME-env/$GIT_REPO
source ../bin/activate
git clone $GIT_URL
pip install -r requirements.txt
echo "=> Git OK"

# nginx
echo "=> Nginx ..."
sudo cp prod/nginx-prod.conf /etc/nginx/sites-available/$SITE_NAME-prod

read -p "Customize /etc/nginx/sites-available/$SITE_NAME-* (do CTRL-Z, edit the file, then \fg)"

sudo ln -s /etc/nginx/sites-available/$SITE_NAME-prod /etc/nginx/sites-enabled/$SITE_NAME
sudo nginx -t
echo "=> Nginx OK"

# gunicorn
echo "=> Gunicorn"
pip install gunicorn
cd /opt/$SITE_NAME-env/$GIT_REPO
cp prod/gunicorn_start.sh .

read -p "Customize gunicorn_start.sh (do CTRL-Z, edit the file, then \fg)"

gunicorn --check-config $SITE_NAME.wsgi
echo "=> Gunicorn OK"

# supervisor
echo "=> Supervisor"

cd /opt/$SITE_NAME-env/$GIT_REPO
sudo cp prod/supervisor.conf /etc/supervisor/conf.d/$SITE_NAME.conf

read -p "Customize /etc/supervisor/conf.d/$SITE_NAME.conf (do CTRL-Z, edit the file, then \fg)"

sudo supervisorctl reread
sudo supervisorctl reload
sudo supervisorctl start $SITE_NAME
echo "=> Supervisor OK"

echo "reloading all"
sudo service nginx restart
sudo service supervisor restart
sudo supervisorctl restart heebari

echo "All done, no errors."

#!/bin/bash

SITE_NAME="wakatime"
USER="nodraak"
GROUP="nodraak"
GIT_REPO="$SITE_NAME"
GIT_URL="https://github.com/Nodraak/$GIT_REPO"

if [ "$(git status -s -uno)" != "" ];
then
    echo "Error, files have been changed. git will fail.";
    exit 1
fi

cd /opt/$SITE_NAME-env/$SITE_NAME-site

# Maintenance mode
sudo rm /etc/nginx/sites-enabled/$SITE_NAME
sudo ln -s /etc/nginx/sites-available/$SITE_NAME-maintenance /etc/nginx/sites-enabled/$SITE_NAME
sudo service nginx reload

# TODO backup

# Update application data
git pull $GIT_URL
source ../bin/activate
pip install --upgrade -r requirements.txt
deactivate

# Restart site
sudo supervisorctl restart $SITE_NAME

# Exit maintenance mode
sudo rm /etc/nginx/sites-enabled/$SITE_NAME
sudo ln -s /etc/nginx/sites-available/$SITE_NAME-prod /etc/nginx/sites-enabled/$SITE_NAME
sudo service nginx reload

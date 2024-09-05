#!/bin/bash

set -e

cd /home/django/turesto

msg() { echo "==== $1 ===="; }

#export GIT_SSH="/var/www/git-ssh.sh"
#export GIT_SSH_KEY="/var/www/.ssh/id_rsa_apply"

msg "Pulling latest changes from GitHub repo"

git pull origin master
#chown -R www-data:www-data . ?

. env/bin/activate

msg "Installing dependencies"

python -m pip install --require-venv --no-cache-dir --exists-action=w -r requirements.txt

msg "Running migrations"

python manage.py migrate

msg "Collecting static files"

python manage.py collectstatic --noinput --link

msg "Restarting services"

systemctl restart gunicorn.turesto
systemctl restart celery.turesto
systemctl restart celerybeat.turesto

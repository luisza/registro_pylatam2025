#!/bin/bash

cd /ecsl

mkdir -p /run/logs/
chown -R ecsl:ecsl /ecsl
runuser -p  -c "python manage.py migrate" ecsl

if [ -z "$DEVELOPMENT" ]; then
  if [ ! -z "$FVAHOSTNAME" ]; then
    sed -i 's/server_name registro.softwarelibre.ca www.registro.softwarelibre.ca;/server_name $ECSLHOSTNAME www.$ECSLHOSTNAME;/g'  /etc/nginx/sites-available/default
  fi
  supervisord -n
else
  runuser -p -c "celery -A ECSL worker -l INFO -B --scheduler django_celery_beat.schedulers:DatabaseScheduler" ecsl &
  runuser -p -c "python manage.py runserver 0.0.0.0:8000" ecsl
fi


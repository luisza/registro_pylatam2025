#!/bin/bash

sudo docker run -d --rm --name ecsl-mail -p 8025:8025 -p  1025:1025 -d mailhog/mailhog
sudo docker run -d --rm --name ecsl-rabbitmq -p 5672:5672 -d rabbitmq:3

echo "Esperando el inicio de rabbitmq ..." && sleep 20

celery -A ECSL worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler 

sudo docker rm -f ecsl-mail
sudo docker rm -f ecsl-rabbitmq

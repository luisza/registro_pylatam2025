#!/bin/bash

docker run -d --rm --name ecsl-mail -p 8025:8025 -p  1025:1025 -d mailhog/mailhog
docker run -d --rm --name ecsl-rabbitmq -p 5672:5672 -d rabbitmq:3

echo "Esperando el inicio de rabbitmq ..." && sleep 20

celery -A ecsl_proj worker -l INFO -B --scheduler django_celery_beat.schedulers:DatabaseScheduler

docker rm -f ecsl-mail
docker rm -f ecsl-rabbitmq

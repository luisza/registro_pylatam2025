# Use an official Python runtime as a parent image
FROM python:3.7-buster
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ENV USER="ecsl"
RUN useradd -u $UID -ms /bin/bash $USER

RUN mkdir -p /run/logs/ /run/static/
WORKDIR /ecsl

RUN apt-get update && \
    apt-get install -y  libxslt-dev libxml2-dev python3-setuptools libmariadbclient-dev libssl-dev nginx supervisor

ADD requirements.txt /ecsl

RUN pip install --upgrade --trusted-host pypi.python.org --no-cache-dir pip requests setuptools gunicorn && \
pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt

RUN apt-get -y autoremove && \
     apt-get -y clean   && \
     rm -rf /var/lib/apt/lists/*

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN sed -i 's/user www-data;/user ecsl;/g' /etc/nginx/nginx.conf

COPY docker/nginx-app.conf /etc/nginx/sites-available/default
COPY docker/supervisor-app.conf /etc/supervisor/conf.d/

ADD src /ecsl

RUN python manage.py collectstatic  --noinput --settings=ECSL.settings

ADD docker/entrypoint.sh /run/
RUN chown -R ecsl:ecsl /run/

RUN chmod +x /run/entrypoint.sh

EXPOSE 80 8000

CMD ["/run/entrypoint.sh"]

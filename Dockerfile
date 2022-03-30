FROM ubuntu:20.04

RUN apt-get update -y && apt-get install -y python3-pip python-dev apt-transport-https ca-certificates curl \
&& apt-get clean autoclean && apt-get autoremove --yes && rm -rf /var/lib/{apt,dpkg,cache,log}

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY webhook.py /app

COPY wsgi.py /app

CMD gunicorn --certfile=/certs/webhook.crt --keyfile=/certs/webhook.key --bind 0.0.0.0:443 wsgi:webhook
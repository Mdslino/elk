FROM python:slim-buster

LABEL maintener="mdslino@gmail.com"

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system

ARG broker_host
ARG broker_port
ARG broker_user
ARG broker_pass

ARG apm_host

ARG gunicorn_log_level
ARG gunicorn_workers

ARG host
ARG port

ENV PORT=$port \
HOST=$host \
BROKER_HOST=$broker_host \
BROKER_PORT=$broker_port \
BROKER_USER=$broker_user \
BROKER_PASS=$broker_pass \
APM_HOST=$apm_host \
GUNICORN_LOG_LEVEL=$gunicorn_log_level \
GUNICORN_WORKERS=$gunicorn_workers

ADD . .

EXPOSE 80

CMD ["python", "app.py"]
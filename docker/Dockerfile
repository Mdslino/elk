FROM python:slim-buster

LABEL maintener="mdslino@gmail.com"

ARG broker_host
ARG broker_port
ARG broker_user
ARG broker_pass
ARG host
ARG port

ENV PORT=$port \
HOST=$host \
BROKER_HOST=$broker_host \
BROKER_PORT=$broker_port \
BROKER_USER=$broker_user \
BROKER_PASS=$broker_pass

WORKDIR /app

RUN pip install --no-cache-dir -U pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system

ADD . .

EXPOSE 80

CMD ["python", "app.py"]
import logging

from decouple import config as get_env
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask, jsonify
from python_logging_rabbitmq import RabbitMQHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

broker_host = get_env("BROKER_HOST", "localhost")
broker_port = get_env("BROKER_PORT", 5672, cast=int)
broker_user = get_env("BROKER_USER", "guest")
broker_pass = get_env("BROKER_PASS", "guest")
apm_url = get_env('APM_HOST', 'http://localhost:8200')

print(apm_url)
rabbit = RabbitMQHandler(
    host=broker_host,
    port=broker_port,
    username=broker_user,
    password=broker_pass,
    exchange="logging",
    routing_key_format="logstash",
)

logger.addHandler(rabbit)

application = Flask(__name__)
application.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'ELK Sample Application',
    'SERVER_URL': apm_url,
    'COLLECT_LOCAL_VARIABLES': 'all',
    'CAPTURE_BODY': 'all',
}
apm = ElasticAPM(application)


@application.route("/")
def health_check():
    logger.info("Health Check")
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    application.run(host=get_env("HOST", "0.0.0.0"), port=get_env("PORT", 8000, cast=int), debug=False)

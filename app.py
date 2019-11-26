import logging
import os

from flask import Flask, jsonify
from python_logging_rabbitmq import RabbitMQHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

broker_host = os.getenv("BROKER_HOST", "localhost")
broker_port = int(os.getenv("BROKER_PORT", 5672))
broker_user = os.getenv("BROKER_USER", "guest")
broker_pass = os.getenv("BROKER_PASS", "guest")

print(broker_host)
print(broker_port)
print(broker_user)
print(broker_pass)

rabbit = RabbitMQHandler(
    host=broker_host,
    port=broker_port,
    username=broker_user,
    password=broker_pass,
    exchange="logging",
    routing_key_format="logstash",
)
logger.addHandler(rabbit)

app = Flask(__name__)


@app.route("/")
def health_check():
    logger.info("Health Check")
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))

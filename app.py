import logging

from decouple import config as get_env
from elasticapm.contrib.flask import ElasticAPM
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from python_logging_rabbitmq import RabbitMQHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

broker_host = get_env("BROKER_HOST", "localhost")
broker_port = get_env("BROKER_PORT", 5672, cast=int)
broker_user = get_env("BROKER_USER", "guest")
broker_pass = get_env("BROKER_PASS", "guest")
apm_url = get_env('APM_HOST', 'http://localhost:8200')

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
application.config['SQLALCHEMY_DATABASE_URI'] = get_env('DB_URI', 'postgres://user:password@localhost:5432/elk')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
migrate = Migrate(application, db)
apm = ElasticAPM(application)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(ModelSchema):
    class Meta:
        model = User


@application.route("/health-check")
def health_check():
    logger.info("Health Check")
    return jsonify({"status": "ok"})


@application.route('/users')
def users():
    users = User.query.all()
    users_serialized = UserSchema().dump(users, many=True)
    return jsonify({'data': users_serialized})

@application.route('/users/<int:user_id>')
def user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    user_serialized = UserSchema().dump(user)
    return user_serialized



if __name__ == "__main__":
    application.run(host=get_env("HOST", "0.0.0.0"), port=get_env("PORT", 8000, cast=int), debug=False)

# ELK Docker Composer
This project is just a example on how to run an ELK stack with RabbitMQ as source to Logstash

If you are on Linux execute the following command before running the ELK stack:

`sudo sysctl -w vm.max_map_count=262144`

To run the ELK stack just execute:

`docker-compose up --build -d app logstash`

Now you can access Kibana on `http://localgost:5601` and the web application on `http://localhost:8000`

Every time you access the web application a log will be send to RabbitMQ and will be consumed by logstash.
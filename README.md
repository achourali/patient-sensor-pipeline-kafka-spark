### Create kafka topics
    bin/kafka-topics.sh --create --topic RawPatientData --bootstrap-server localhost:9092
    bin/kafka-topics.sh --create --topic JsonPatientData --bootstrap-server localhost:9092
### Consume kafka events
    bin/kafka-console-consumer.sh --topic RawPatientData --from-beginning --bootstrap-server localhost:9092
    bin/kafka-console-consumer.sh --topic JsonPatientData --from-beginning --bootstrap-server localhost:9092

### Start patient sensor api
    python3 patient_sensor.py

### Start kafka server
    bin/kafka-server-start.sh config/server.properties

### Send (random) raw data to kafka
    python3 send_data_to_kafka.py

### Process -> ( save in mongo and stream processed data ) with spark
    python3 spark.py

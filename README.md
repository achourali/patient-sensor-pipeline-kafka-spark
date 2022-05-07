### Create kafka topic
    bin/kafka-topics.sh --create --topic RawPatientData --bootstrap-server localhost:9092
### Consume kafka events
    bin/kafka-console-consumer.sh --topic RawPatientData --from-beginning --bootstrap-server localhost:9092
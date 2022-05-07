import json
from bson import json_util
from dateutil import parser
from pyspark import SparkContext
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient

mongoClient = MongoClient('localhost', 27017)
db = mongoClient['patientsData']
collection = db['RealTimeData']

def data_exist(patient_id, timestamp):
    return collection.count_documents({
        "$and": [
            {'timestamp': {"$eq": timestamp}},
            {'patient_id': {"$eq": patient_id}}
        ]

    }) > 0

def structuring_data(msg):
    patient_data_dict = {}

    # Create RDD (Resilient Distributed Dataset) from a list data
    rdd = sc.parallelize(msg.value.decode("utf-8").split())

    patient_data_dict["RawData"] = str(msg.value.decode("utf-8"))

    try:
        # rdd.collect() : retriev the data from the dataframe
        patient_data_dict["patient_id"] = int(rdd.collect()[0])
    except Exception as error:
        patient_data_dict["patient_id"] = None

    try:
        patient_data_dict["timestamp"] = parser.isoparse(rdd.collect()[1])
    except Exception as error:
        patient_data_dict["timestamp"] = None

    try:
        patient_data_dict["battery_life"] = int(rdd.collect()[2])
    except Exception as error:
        patient_data_dict["battery_life"] = None

    try:
        patient_data_dict["heart_beat"] = int(rdd.collect()[3])
    except Exception as error:
        patient_data_dict["heart_beat"] = None

    try:
        patient_data_dict["systolic_blood_pressure"] = int(rdd.collect()[4])
    except Exception as error:
        patient_data_dict["systolic_blood_pressure"] = None

    try:
        patient_data_dict["diastolic_blood_pressure"] = int(rdd.collect()[5])
    except Exception as error:
        patient_data_dict["diastolic_blood_pressure"] = None

    return patient_data_dict


def consume_stream_data():

    for msg in consumer:
        if msg.value.decode("utf-8") != "Error in Connection":
            dict_data = structuring_data(msg)

            if data_exist(dict_data['patient_id'], dict_data['timestamp']) == False:
                # save data in mongodb
                collection.insert_one(dict_data)
                producer.send("JsonPatientData", json.dumps(
                    dict_data, default=json_util.default).encode('utf-8'))

            print(dict_data)

# Get or instantiate a SparkContext and register it as a singleton object :
sc = SparkContext.getOrCreate()

# Control our logLevel. Valid log levels include: "ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN"
sc.setLogLevel("WARN")

# Consume records from a Kafka cluster :
consumer = KafkaConsumer('RawPatientData', auto_offset_reset='earliest', bootstrap_servers=[
                         'localhost:9092'], consumer_timeout_ms=10000)

# Kafka client that publishes records to the Kafka cluster :
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

consume_stream_data()

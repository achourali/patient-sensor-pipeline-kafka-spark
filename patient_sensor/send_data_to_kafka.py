import time
import json
import requests
import datetime
from kafka import KafkaProducer, KafkaClient
from websocket import create_connection

def get_patient_data(patient_id):
    
    try:
        url = 'http://0.0.0.0:3030/patient_data/{0}'.format(patient_id)
        r = requests.get(url)
        return r.text
    except:
        return "Error in Connection"


producer = KafkaProducer(bootstrap_servers=['kafka:9092'])
patients_number=3


while True:
    time.sleep(1)
    for id in range(patients_number):
        msg =  get_patient_data(id)
        producer.send("RawPatientData", msg.encode('utf-8'))
        


    


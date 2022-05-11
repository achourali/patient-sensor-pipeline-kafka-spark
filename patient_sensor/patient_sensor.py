
import time
import random
from datetime import datetime
from flask import Flask, Response

app = Flask(__name__)

# This Route Generates random patient data :

@app.route('/patient_data/<patient_id>')
def get_sensor_data(patient_id):
    
    timestamp = str(time.time())
    systolic_blood_pressure = str(int(random.uniform(60, 200)))
    diastolic_blood_pressure = str(int(random.uniform(40, 150)))
    battery_life = str(int(random.uniform(100, 0)))
    heart_beat = str(int(random.uniform(30, 160)))

    response = "{patient_id} {timestamp} {battery_life} {heart_beat} {systolic_blood_pressure} {diastolic_blood_pressure}\
                ".format(
        patient_id=patient_id,
        timestamp=timestamp,
        battery_life=battery_life,
        heart_beat=heart_beat,
        systolic_blood_pressure=systolic_blood_pressure,
        diastolic_blood_pressure=diastolic_blood_pressure,
    )

    return Response(response, mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3030')

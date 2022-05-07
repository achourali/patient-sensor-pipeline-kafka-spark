
import time
import random
from datetime import datetime
from flask import Flask, Response

app = Flask(__name__)

# data


@app.route('/patient_data/<patient_id>')
def get_sensor_data(patient_id):
    print(patient_id)
    timestamp = "{}".format((datetime.now()).now().isoformat())
    systolic_blood_pressure = str(round(random.uniform(60, 200), 0))
    diastolic_blood_pressure = str(round(random.uniform(40, 150), 0))
    battery_life = str(round(random.uniform(100, 0), 0))
    heart_beat = str(round(random.uniform(30, 160), 0))

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

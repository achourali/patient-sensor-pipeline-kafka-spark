import random
import pandas as pd
from bokeh.driving import count
from bokeh.models import ColumnDataSource
from kafka import KafkaConsumer
from bokeh.plotting import curdoc, figure
from bokeh.models import DatetimeTickFormatter
from bokeh.models.widgets import Div
from bokeh.layouts import column, row
import ast
import time
import pytz
from datetime import datetime
import colorcet as cc


@count()
def update(i):
    for event in consumer:
        break

    event = ast.literal_eval(event.value.decode("utf-8"))

    plot = get_patient_plot(event["patient_id"])

    x = datetime.strptime(event["timestamp"]["$date"],
                          '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()
    x = datetime.fromtimestamp(x, tz).isoformat()
    x = pd.to_datetime(x)
    plot["div"].text = "<h2>Patient {id}</h2> <br> battery :{battery}%".format(
        id=event["patient_id"], battery=event["battery"])

    plot["sources"]["heart_beat_src"].stream(
        {"x": [x], "y": [event["heart_beat"]]}, ROLLOVER)
    plot["sources"]["systolic_blood_pressure_src"].stream(
        {"x": [x], "y": [event["systolic_blood_pressure"]]}, ROLLOVER)
    plot["sources"]["diastolic_blood_pressure_src"].stream(
        {"x": [x], "y": [event["diastolic_blood_pressure"]]}, ROLLOVER)


def get_patient_plot(patient_id):
    patient_plot = None
    for plot in plots:
        if plot["patient_id"] == patient_id:
            patient_plot = plot
            break
    if(patient_plot == None):

        div = Div(
            text="<h2>Patient {id}</h2>".format(id=str(patient_id)),
            width=90,
            height=35
        )
        heart_beat_fig = figure(title="heart beat",
                                x_axis_type="datetime")

        heart_beat_src = ColumnDataSource({"x": [], "y": []})
        heart_beat_fig.line("x", "y", source=heart_beat_src,
                            color=cc.glasbey_dark[0])

        systolic_blood_pressure_fig = figure(title="systolic blood pressure",
                                             x_axis_type="datetime")

        systolic_blood_pressure_src = ColumnDataSource({"x": [], "y": []})
        systolic_blood_pressure_fig.line("x", "y", source=systolic_blood_pressure_src,
                                         color=cc.glasbey_dark[1])

        diastolic_blood_pressure_fig = figure(title="diastolic blood pressure",
                                              x_axis_type="datetime")

        diastolic_blood_pressure_src = ColumnDataSource({"x": [], "y": []})
        diastolic_blood_pressure_fig.line("x", "y", source=diastolic_blood_pressure_src,
                                          color=cc.glasbey_dark[1])

        patient_plot = {"patient_id": patient_id,
                        "sources": {"heart_beat_src": heart_beat_src,
                                    "systolic_blood_pressure_src": systolic_blood_pressure_src,
                                    "diastolic_blood_pressure_src": diastolic_blood_pressure_src,
                                    },
                        "div": div
                        }
        plots.append(patient_plot)

        doc.add_root(
            row(children=[
                div,
                heart_beat_fig,
                systolic_blood_pressure_fig,
                diastolic_blood_pressure_fig]
                )
        )

    return patient_plot


UPDATE_INTERVAL = 500
ROLLOVER = 10
plots = []
tz = pytz.timezone('Africa/Tunis')
source = ColumnDataSource({"x": [], "y": []})
consumer = KafkaConsumer('JsonPatientData', auto_offset_reset='latest', bootstrap_servers=[
                         'kafka:9092'], consumer_timeout_ms=20000)
doc = curdoc()

doc.add_periodic_callback(update, UPDATE_INTERVAL)

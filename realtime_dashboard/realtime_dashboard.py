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
from functools import partial
from threading import Thread, Lock
import json


def updatePatientData(event):

    event = ast.literal_eval(event.value.decode("utf-8"))

    plot = get_patient_plot(int(event["patient_id"]))
    x = datetime.fromtimestamp(event["timestamp"], tz).isoformat()
    x = pd.to_datetime(x)
    plot["div"].text = "<h2>Patient {id}</h2> <br> battery :{battery}%".format(
        id=event["patient_id"], battery=event["battery"])

    plot["sources"]["heart_beat_src"].stream(
        {"x": [x], "y": [event["heart_beat"]]}, ROLLOVER)
    plot["sources"]["systolic_blood_pressure_src"].stream(
        {"x": [x], "y": [event["systolic_blood_pressure"]]}, ROLLOVER)
    plot["sources"]["diastolic_blood_pressure_src"].stream(
        {"x": [x], "y": [event["diastolic_blood_pressure"]]}, ROLLOVER)


def updatePatientsStats(event):
    event = ast.literal_eval(event.value.decode("utf-8"))
    for patient_index in event["patient_id"]:
        patient_id=event["patient_id"][patient_index]
        plot = get_patient_plot(int(patient_id))
        
        text="<h2>Stats</h2>"
        for stat_label in event:
            text+="{stat_label} : {value} <br>".format(stat_label=stat_label,value=int(event[stat_label][patient_index]))
        plot["stats_div"].text = text;
        
            
    


def consumePatientData():
    for event in patientDataConsumer:
        doc.add_next_tick_callback(partial(updatePatientData, event=event))


def consumePatientsStats():
    for event in patientsStatsConsumer:
        doc.add_next_tick_callback(partial(updatePatientsStats, event=event))


def get_patient_plot(patient_id):
    with critical_function_lock:
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

            stats_div = Div(
                text="",
                width=250,
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
                            "div": div,
                            "stats_div": stats_div
                            }
            plots.append(patient_plot)

            doc.add_root(
                row(children=[
                    div,
                    stats_div,
                    heart_beat_fig,
                    systolic_blood_pressure_fig,
                    diastolic_blood_pressure_fig]
                    )
            )
        return patient_plot


ROLLOVER = 10

plots = []

tz = pytz.timezone('Africa/Tunis')

source = ColumnDataSource({"x": [], "y": []})

patientDataConsumer = KafkaConsumer('JsonPatientData', auto_offset_reset='latest', bootstrap_servers=[
    'kafka:9092'], consumer_timeout_ms=20000)

patientsStatsConsumer = KafkaConsumer('JsonPatientsStats', auto_offset_reset='latest', bootstrap_servers=[
    'kafka:9092'], consumer_timeout_ms=20000)

doc = curdoc()

critical_function_lock = Lock()

thread = Thread(target=consumePatientData)
thread.start()


thread = Thread(target=consumePatientsStats)
thread.start()

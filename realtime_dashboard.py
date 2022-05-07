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
    print(event["patient_id"], len(plots))

    plot["sources"]["heart_beat_src"].stream(
        {"x": [i], "y": [event["heart_beat"]]}, ROLLOVER)


def get_patient_plot(patient_id):
    patient_plot = None
    for plot in plots:
        if plot["patient_id"] == patient_id:
            patient_plot = plot
            break
    if(patient_plot == None):
        fig = figure(title="Patient "+str(patient_id),
                     x_axis_type="datetime", plot_width=1000)

        heart_beat_src = ColumnDataSource({"x": [], "y": []})
        fig.line("x", "y", source=heart_beat_src, color=cc.glasbey_dark[0])
        patient_plot = {"patient_id": patient_id,
                        "sources": {"heart_beat_src": heart_beat_src}}
        plots.append(patient_plot)

        doc.add_root(
            row(children=[div, fig])
        )

    return patient_plot


UPDATE_INTERVAL = 0
ROLLOVER = 10

plots = []

source = ColumnDataSource({"x": [], "y": []})
consumer = KafkaConsumer('JsonPatientData', auto_offset_reset='latest', bootstrap_servers=[
                         'localhost:9092'], consumer_timeout_ms=20000)
div = Div(
    text='',
    width=120,
    height=35
)


doc = curdoc()

doc.add_periodic_callback(update, UPDATE_INTERVAL)

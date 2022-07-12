from django.shortcuts import render
from django.http import HttpResponse
from models import senors


def index(request):
    sensor_readings = sensors.objects.all()
    for x in sensor_readings:
        val = str(sensor.value)
    html = ''
    return HttpResponse("Hello, world!")
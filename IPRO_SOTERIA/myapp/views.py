from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import sensors_table
from django.contrib.auth.decorators import login_required

#Renders the 'index' page and sends along all the data from the database needed to construct the table
@login_required
def index(request):
    sensor_readings = sensors_table.objects.all()
    return render(request,"index.html",{'sensor_readings':sensor_readings})
#Returns a json-formatted database query response so that the table can be updated without refreshing the page
def getReadings(request):
    sensor_readings = sensors_table.objects.all()
    sensor_readings_json = serializers.serialize('json',sensor_readings)
    return HttpResponse(sensor_readings_json)

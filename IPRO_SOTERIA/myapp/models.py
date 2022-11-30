from django.db import models

class sensors_table(models.Model):
    ip_id = models.CharField(max_length=64, blank=True, primary_key=True)
    sensor = models.CharField(max_length=32, blank=True)
    value = models.CharField(max_length=16,null=True)
    time = models.CharField(max_length=64,null=True)
    status = models.CharField(max_length=64,null=True) 
    #status = models.CharField(max_length=64,null=True)

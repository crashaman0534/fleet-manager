from django.db import models

# Create your models here.
class DeviceModel(models.Model):
    vin = models.CharField(max_length=17)
    ip = models.CharField(max_length=15)
    port = models.CharField(max_length=10)

    def __str__(self):
        return self.vin

class TopicModel(models.Model):
    name = models.CharField(max_length=100)
    isPub = models.BooleanField(default=False)
    isSub = models.BooleanField(default=True)

    def __str__(self):
        return self.name

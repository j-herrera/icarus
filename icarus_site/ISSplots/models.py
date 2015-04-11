from django.db import models

class TLE:
	mean_anomaly = models.FloatField(default=0)

class ISSData:
	latitude = models.FloatField(default=0)


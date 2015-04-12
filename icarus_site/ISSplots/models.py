from django.db import models

class TLE:
	epochYear = models.IntegerField(default=0)
	epoch = models.FloatField(default=0)
	inc = models.FloatField(default=0)
	raan = models.FloatField(default=0)
	ecc = models.FloatField(default=0)
	aper = models.FloatField(default=0)
	ma = models.FloatField(default=0)
	mm = models.FloatField(default=0)	

class ISSData:
	lat = models.FloatField(default=0)
	lon = models.FloatField(default=0)
	alt = models.FloatField(default=0)
	vel = models.FloatField(default=0)


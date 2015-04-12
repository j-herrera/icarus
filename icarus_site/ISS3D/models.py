from django.db import models

class TLE:
	inc = models.FloatField(default=0)
	raan = models.FloatField(default=0)
	ecc = models.FloatField(default=0)
	aper = models.FloatField(default=0)
	ma = models.FloatField(default=0)
	mm = models.FloatField(default=0)

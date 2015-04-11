from django.db import models

class ISSposition(models.Model):
	lat = models.FloatField(default=0)
	lon = models.FloatField(default=0)
	
	def __str__(self):
		return "lat: " + str(self.lat) + ", lon: " + str(self.lon)

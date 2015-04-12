from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import pycurl
import json
from io import BytesIO

from geojson import Feature, Point

from .models import ISSposition

def map(request):
	return render(request, 'ISStrace/map.html')

def getPos(request):
	c = pycurl.Curl()
	data = BytesIO()

	c.setopt(pycurl.SSL_VERIFYHOST, 0)
	c.setopt(pycurl.SSL_VERIFYPEER, 0)
	c.setopt(pycurl.URL, 'https://api.wheretheiss.at/v1/satellites/25544')
	c.setopt(c.WRITEDATA, data)

	c.perform()
	c.close()

	dictionary = json.loads(data.getvalue().decode())
	
	#point = Point((-4.289904821807117, 55.86766270695622))
	point = Point((dictionary['longitude'], dictionary['latitude']))
	geop = Feature(geometry=point, properties={"alt":  dictionary['altitude'], "vel":  dictionary['velocity']})
	return JsonResponse(geop, safe=False)

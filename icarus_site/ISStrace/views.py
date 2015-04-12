from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import urllib3
import json

from geojson import Feature, Point

from .models import ISSposition

def map(request):
	return render(request, 'ISStrace/map.html')

def getPos(request):
	http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
	r = http.request('GET', 'https://api.wheretheiss.at/v1/satellites/25544')

	dictionary = json.loads(r.data.decode())
	
	#point = Point((-4.289904821807117, 55.86766270695622))
	point = Point((dictionary['longitude'], dictionary['latitude']))
	geop = Feature(geometry=point, properties={"alt":  dictionary['altitude'], "vel":  dictionary['velocity']})
	return JsonResponse(geop, safe=False)

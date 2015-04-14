from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import urllib3
import json
import math as mth

from geojson import Feature, Point

from .models import ISSposition

def map(request):
	return render(request, 'ISStrace/map.html')

def mapSim(request):
	return render(request, 'ISStrace/mapSim.html')

def getPos(request):
	http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
	r = http.request('GET', 'https://api.wheretheiss.at/v1/satellites/25544')

	dictionary = json.loads(r.data.decode())
	
	#point = Point((-4.289904821807117, 55.86766270695622))
	point = Point((dictionary['longitude'], dictionary['latitude']))
	geop = Feature(geometry=point, properties={"alt":  dictionary['altitude'], "vel":  dictionary['velocity']})
	return JsonResponse(geop, safe=False)

def getProjAndPos(request):
	http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
	r = http.request('GET', 'https://api.wheretheiss.at/v1/satellites/25544')
	r2 = http.request('GET', 'https://api.wheretheiss.at/v1/satellites/25544/tles')

	dictionary = json.loads(r.data.decode())
	dictionary2 = json.loads(r2.data.decode())
	
	line2 = dictionary2['line2']
	inc = float(line2[9:16])
	raan = float(line2[18:25])
	ecc = float('0.'+line2[26:33])
	aper = float(line2[34:42])
	ma = float(line2[43:51])
	mm = float(line2[52:63])

	J2 = 1.08262668e-3
	REarth = 6.371e6
	muEarth = 398600.4418e9

	mm_rad = mm * mth.pi / 43200.0
	inc_rad = inc * mth.pi / 180.0
	p = (muEarth / mm_rad * mm_rad)**(1.0/3.0)
	p *= (1.0 - ecc * ecc)
 
	dRaanByDt = -1.5 * mm_rad * J2 * REarth**2 / p**2
	dAperByDt = 2.0 * dRaanByDt * (1.25 * mth.sin(inc_rad)**2 - 1.0)
	dRaanByDt *= mth.cos(inc_rad) * 180.0 / mth.pi
	
	#point = Point((-4.289904821807117, 55.86766270695622))
	point = Point((dictionary['longitude'], dictionary['latitude']))
	geop = Feature(geometry=point, properties={"alt":  dictionary['altitude'],
		"vel":  dictionary['velocity'], "inc":inc, "raan":raan, "aper":aper,
		"ma":ma, "mm":mm, "dRaan":dRaanByDt, "dAper":dAperByDt})
	return JsonResponse(geop, safe=False)

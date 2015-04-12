from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import urllib3
import json
from geojson import Feature, Point

from .models import TLE
from .models import ISSData

def plot(request):
	return render(request, 'ISSplots/plot.html')

def getISSData(request):
	http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
	r = http.request('GET', 'https://api.wheretheiss.at/v1/satellites/25544/tles')

	dictionary = json.loads(r.data.decode())
	
	line2 = dictionary['line2']
	
	inc = float(line2[8:16])
	raan = float(line2[17:25])
	ecc = float('0.' + line2[26:33])
	aper = float(line2[34:42])
	ma = float(line2[43:51])
	mm = float(line2[52:63])
	
	r = http.request('GET', 'https://api.wheretheiss.at/v1/satellites/25544')

	dictionary = json.loads(r.data.decode())
	
	lat = dictionary['latitude']
	lon = dictionary['longitude']
	alt = dictionary['altitude']
	vel = dictionary['velocity']

	return JsonResponse({'inc':inc,
		'raan':raan, 'ecc':ecc, 'aper':aper, 'ma':ma, 'mm':mm,
		'lat':lat, 'lon':lon, 'alt':alt, 'vel':vel}, safe=False)

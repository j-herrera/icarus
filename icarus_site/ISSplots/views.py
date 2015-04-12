from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import pycurl
import json
from io import BytesIO
from geojson import Feature, Point

from .models import TLE
from .models import ISSData

def plot(request):
	return render(request, 'ISSplots/plot.html')

def getISSData(request):
	c = pycurl.Curl()
	data = BytesIO()

	c.setopt(pycurl.SSL_VERIFYHOST, 0)
	c.setopt(pycurl.SSL_VERIFYPEER, 0)
	c.setopt(pycurl.URL, 'https://api.wheretheiss.at/v1/satellites/25544/tles')
	c.setopt(c.WRITEDATA, data)

	c.perform()
	c.close()

	dictionary = json.loads(data.getvalue().decode())
	
	line2 = dictionary['line2']
	
	inc = float(line2[8:16])
	raan = float(line2[17:25])
	ecc = float('0.' + line2[26:33])
	aper = float(line2[34:42])
	ma = float(line2[43:51])
	mm = float(line2[52:63])

	c = pycurl.Curl()
	data = BytesIO()

	c.setopt(pycurl.SSL_VERIFYHOST, 0)
	c.setopt(pycurl.SSL_VERIFYPEER, 0)
	c.setopt(pycurl.URL, 'https://api.wheretheiss.at/v1/satellites/25544')
	c.setopt(c.WRITEDATA, data)

	c.perform()
	c.close()

	dictionary = json.loads(data.getvalue().decode())
	
	lat = dictionary['latitude']
	lon = dictionary['longitude']
	alt = dictionary['altitude']
	vel = dictionary['velocity']

	return JsonResponse({'inc':inc,
		'raan':raan, 'ecc':ecc, 'aper':aper, 'ma':ma, 'mm':mm,
		'lat':lat, 'lon':lon, 'alt':alt, 'vel':vel}, safe=False)

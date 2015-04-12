from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import pycurl
import json
from io import BytesIO

from .models import TLE

def Dplot(request):
	return render(request, 'ISS3D/Dplot.html')

def getTLE(request):
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
	inc = float(line2[9:16])
	raan = float(line2[18:25])
	ecc = float('0.'+line2[26:33])
	aper = float(line2[34:42])
	mm = float(line2[52:63])

	return JsonResponse({'inc': inc, 'raan': raan, 'ecc': ecc, 'aper': aper, 'mm':mm}, safe=False)

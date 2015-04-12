from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import urllib3
import json

from .models import TLE

def Dplot(request):
	return render(request, 'ISS3D/Dplot.html')

def getTLE(request):
	http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
	r = http.request('GET', 'https://api.wheretheiss.at/v1/satellites/25544/tles')

	dictionary = json.loads(r.data.decode())
	
	line2 = dictionary['line2']
	inc = float(line2[9:16])
	raan = float(line2[18:25])
	ecc = float('0.'+line2[26:33])
	aper = float(line2[34:42])
	mm = float(line2[52:63])

	return JsonResponse({'inc': inc, 'raan': raan, 'ecc': ecc, 'aper': aper, 'mm':mm}, safe=False)

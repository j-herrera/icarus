from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import math as mth

import urllib3
import json

from .models import TLE

def Dplot(request):
	return render(request, 'ISS3D/Dplot.html')

def Dsym(request):
	return render(request, 'ISS3D/Dsym.html')

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

def getJ2TLE(request):
	http = urllib3.PoolManager(cert_reqs='CERT_NONE', assert_hostname=False)
	r = http.request('GET', 'https://api.wheretheiss.at/v1/satellites/25544/tles')

	dictionary = json.loads(r.data.decode())
	
	line2 = dictionary['line2']
	inc = float(line2[9:16])
	raan = float(line2[18:25])
	ecc = float('0.'+line2[26:33])
	aper = float(line2[34:42])
	mm = float(line2[52:63])

	J2 = 1.08262668e-3
	REarth = 6.378137e6
	muEarth = 398600.4418e9

	mm_rad = mm * mth.pi / 43200.0
	inc_rad = inc * mth.pi / 180.0
	p = (muEarth / mm_rad * mm_rad)**(1.0/3.0)
	p *= (1.0 - ecc * ecc)
 
	dRaanByDt = -1.5 * mm_rad * J2 * REarth**2 / p**2
	dAperByDt = 2.0 * dRaanByDt * (1.25 * mth.sin(inc_rad)**2 - 1.0) * 180.0 / mth.pi
	dRaanByDt *= mth.cos(inc_rad) * 180.0 / mth.pi

	return JsonResponse({'inc':inc,'raan': raan, 'ecc': ecc, 'aper': aper, 'mm':mm,
		'dRaanByDt':dRaanByDt, 'dAperByDt':dAperByDt}, safe=False)

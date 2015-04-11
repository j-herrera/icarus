from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

import pycurl
import json
from io import BytesIO

from .models import TLE

def plot(request):
	return render(request, 'ISSplots/plot.html')

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
	
	ma = line2[43:52]
	return HttpResponse(ma)

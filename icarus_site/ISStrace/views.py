from django.shortcuts import render
from django.http import HttpResponse

from .models import ISSposition

def map(request):
	return render(request, 'ISStrace/map.html')

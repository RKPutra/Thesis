from django.http import HttpResponse
from django.shortcuts import render
import csv
import io

def index(request):
    return render(request, 'login.html')

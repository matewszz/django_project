from urllib import request

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse('HOME 1')

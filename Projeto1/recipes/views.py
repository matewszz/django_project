from django.http import HttpResponse


def home (request):
    return HttpResponse('home')

def contato (request):
    return HttpResponse('contato')

def sobre (request):
    return HttpResponse('sobre')

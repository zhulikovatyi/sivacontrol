from django.template import RequestContext, loader
from django.shortcuts import render

from models import Banner

def index(request):
    banners = Banner.objects.all()
    context = {
        'banners': banners
    }
    return render(request, 'index.html', context)
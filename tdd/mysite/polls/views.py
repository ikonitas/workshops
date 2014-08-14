# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

from .models import Poll


def home(request):
    polls = Poll.objects.all()
    return render(request, "home.html", dict(polls=polls))
    #response = ''
    #for p in polls:
    #    response += p.question
    #return HttpResponse(response)


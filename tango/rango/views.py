from django.shortcuts import render

from django.http import HttpResponse

def index(request):
   return HttpResponse("Rango says.. hello world <br/> <a href = '/rango/about/'>About</a><br/><br/> ")

def about(request):
    return HttpResponse("Rango says here is the about page <br/> <a href = '/rango'>Index</a><br/><br/> This tutorial has been put together by Rhianna Scott, 2084246S")

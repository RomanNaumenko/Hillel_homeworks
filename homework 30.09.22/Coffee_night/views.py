from django.shortcuts import render
from django.http import HttpResponse
import models


# Create your views here.
def route_filter(request, route_type=None, country=None, location=None):
    print("route_type: ", route_type)
    print("country: ", country)
    print("location: ", location)
    return HttpResponse("Hello, world!")


def route_detailes(request):
    pass


def route_reviews(request):
    pass


def route_add(request):
    pass


def add_event(request):
    pass


def event_handler(request, event_id):
    pass

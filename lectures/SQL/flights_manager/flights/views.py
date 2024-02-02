from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Flight, Passengers


def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    fly = Flight.objects.get(pk=flight_id)
    return render(request, "flights/flight.html", {
        "flight": fly,
        "passengers": fly.passenger.all(),
        "non_passengers": Passengers.objects.exclude(flights=fly)
    })


def book(request, flight_id):
    if request.method == 'POST':
        fly = Flight.objects.get(pk=flight_id)
        passenger = Passengers.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(fly)
        return HttpResponseRedirect(reverse("flight", args=(flight_id, )))

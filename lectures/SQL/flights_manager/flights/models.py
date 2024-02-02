from django.db import models


class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departure")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} -> {self.destination}"


class Passengers(models.Model):
    first = models.CharField(max_length=64)
    second = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passenger")

    def __str__(self):
        return f"{self.first} {self.second}"

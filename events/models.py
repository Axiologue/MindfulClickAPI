from django.db import models


class Location(models.Model):
    # Identifying Name
    name = models.CharField(max_length=150)
   
    # Address info
    street_address = models.CharField(max_length=250)
    city = models.CharField(max_length=75)
    postal_code = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    # When/Where
    location = models.ForeignKey(Location)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.name, self.start)

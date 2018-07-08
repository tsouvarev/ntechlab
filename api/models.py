from django.contrib.gis.db.models import PointField
from django.db import models


class Neighbour(models.Model):
    name = models.CharField(max_length=255)
    point = PointField()


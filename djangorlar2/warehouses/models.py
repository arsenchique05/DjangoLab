from django.db import models
from abstracts.models import AbstractSoftDeletableModel


class Warehouse(AbstractSoftDeletableModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Box(AbstractSoftDeletableModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='boxes')
    color = models.CharField(max_length=50)
    weight = models.FloatField()

    def __str__(self):
        return f"{self.color} box ({self.weight} kg)"

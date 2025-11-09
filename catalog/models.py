from django.db import models

class Order(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title

class Unit(models.Model)
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title 
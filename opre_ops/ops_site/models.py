from django.contrib import admin
from django.db import models

class Agency(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "agencies"


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="Role Name")


DIVSIONS = [("1,","DCFD"), ("2", "DDI"), ("3", "DEI"), ("4", "DFS"), ("5", "OD")]
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roles = models.ManyToManyField(Role)
    division = models.CharField(max_length=5, choices=DIVSIONS)

    class Meta:
        verbose_name_plural = "People"

    @property
    def display_name(self):
        return "{} {}".format(self.first_name, self.last_name)

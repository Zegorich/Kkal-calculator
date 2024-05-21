from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=50)
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    desired_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    telegram = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Weight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=1)
    fat = models.DecimalField(max_digits=5, decimal_places=1)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=1)
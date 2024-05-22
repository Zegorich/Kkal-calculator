from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse, reverse_lazy


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

    def get_absolute_url(self):
        return reverse('cat', kwargs={'cat_slug': self.slug})

class Product(models.Model):
    name = models.CharField(max_length=100)
    calories = models.DecimalField(max_digits=5, decimal_places=1)
    protein = models.DecimalField(max_digits=5, decimal_places=1)
    fat = models.DecimalField(max_digits=5, decimal_places=1)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=1)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

class Category(models.Model):
    name = models.TextField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


#class UserProduct(models.Model):
#    user = models.ForeignKey('User', on_delete=models.CASCADE)
#    name = models.CharField(max_length=100)
#    calories = models.DecimalField(max_digits=5, decimal_places=1)
#    protein = models.DecimalField(max_digits=5, decimal_places=1)
#    fat = models.DecimalField(max_digits=5, decimal_places=1)
#    carbohydrates = models.DecimalField(max_digits=5, decimal_places=1)

class UserNutrition(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    meal = models.PositiveSmallIntegerField()
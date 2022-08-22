from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100)


class Toys(models.Model):
    categories = models.ManyToManyField(Category, related_name='toys')
    name = models.CharField(max_length=50)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to="media", null=True)
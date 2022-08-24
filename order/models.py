
from django.db import models

from toys.models import Toy
from accounts.models import User


class Order(models.Model):
    toys = models.ForeignKey(Toy, on_delete=models.CASCADE,
                             related_name='orders')
    phone = models.CharField(max_length=13)
    address = models.TextField()
    city = models.CharField(max_length=100)
    email = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'{self.email} - {self.phone}'
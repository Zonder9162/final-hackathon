from django.db import models
from django.contrib.auth import get_user_model
from toys.models import Toy
# from accounts.models import User


User = get_user_model()

class Order(models.Model):

    STATUS = (
        ('new', 'new order'),
        ('pending', 'pending order'),
        ('finished', 'finished order'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')                         
    phone = models.CharField(max_length=13)
    address = models.TextField()
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=250, default='new')
    

    def __str__(self):
        return f'{self.user} - {self.phone}'


class OrderToys(models.Model):
    toys = models.ForeignKey(Toy, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
from django.db import models
from django.contrib.auth import get_user_model
from toys.models import Toy

from config.celery import app
from django.core.mail import send_mail


User = get_user_model()

class Order(models.Model):

    STATUS = (
        ('new', 'new order'),
        ('pending', 'pending order'),
        ('finished', 'finished order'),
    )

    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')                         
    phone = models.CharField(max_length=13)
    address = models.TextField()
    city = models.CharField(max_length=100)
    email = models.ForeignKey(User,on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=250, default='new')
    

    def __str__(self):
        return f'{self.email} - {self.phone}'

    @staticmethod
    def order_created(self):
        order_created.delay(self.id)


class OrderToys(models.Model):
    toys = models.ForeignKey(Toy, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()



@app.task
def order_created(order_id):
    """
    Task to send e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'You have successfully placed an order.\
                Your order id is {}.'.format(order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent

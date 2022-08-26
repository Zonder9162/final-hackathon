from django.contrib import admin

from .models import Order, OrderToys

admin.site.register(Order)
admin.site.register(OrderToys)
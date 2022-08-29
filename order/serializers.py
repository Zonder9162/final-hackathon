# from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Order

# User = get_user_model()

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        print('CREATING ORDER WITH DATA:', validated_data)
        return Order.objects.order_created(**validated_data)

    def save(self):
        data = self.validated_data
        order = Order.objects.order_created(**data)
        order.order_created()
from django.http import HttpResponse

from django.shortcuts import render, redirect
from rest_framework.permissions import  IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .permissions import IsAuthor
from toys.models import Toy
from .models import Order
from rest_framework import mixins
from .serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin, 
                    GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

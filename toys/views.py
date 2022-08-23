from django.shortcuts import render
from http.client import HTTPResponse
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, filters
from rest_framework.decorators import action, api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response


from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

import toys

from .models import Toy, Category, Comment, Like, Rating
from .serializers import ToySerializer, CategorySerializer, CommentSerializer, FavoriteSerializer
from .permissions import IsAuthor
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *


class ToyViewSet(ModelViewSet):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'price']
    

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('name', openapi.IN_QUERY, 'search toy by name', type=openapi.TYPE_STRING)])


    @action(methods=['GET'], detail=False)
    def search(self, request):
        name = request.query_params.get('name')
        queryset = self.get_queryset()
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        serializer = ToySerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, 200)


    @action(methods=['GET'], detail=False)
    def order_by_rating(self, request):
        queryset = sorted(self.get_queryset(), key=lambda toys: toys.average_rating, reverse=True)
        queryset = self.paginate_queryset(queryset)
        serializer = ToySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, 200)



class CategoryViewSet(mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    mixins.ListModelMixin, 
                    GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class CommentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



@api_view(['GET'])
def toggle_like(request, t_id):
    user = request.user
    toys = get_object_or_404(Toy, id=t_id)

    if Like.objects.filter(user=user,toys=toys).exists():
        Like.objects.filter(user=user, toys=toys).delete()
    else:
        Like.objects.create(user=user, toys=toys)
    return Response("Like toggled", 200)

@api_view(['POST'])
def add_rating(request, t_id):
    user = request.user
    toys = get_object_or_404(Toy, id=t_id)
    value = request.POST.get('value')

    if not user.is_authenticated:
        raise ValueError("Authentication credentials are not provided")

    if not value:
        raise ValueError("Value is required")

    if Rating.objects.filter(user=user, toys=toys).exists():
        rating = Rating.objects.get(user=user, toys=toys)
        rating.value = value
        rating.save()
    else:
        Rating.objects.create(user=user,toys=toys, value=value)

    return Response('Rating created', 201)

@api_view(['GET'])
def add_to_favorite(request, t_id):
    user = request.user
    toys = get_object_or_404(Toy, id=t_id)

    if Favorite.objects.filter(user=user, toys=toys).exists():
        Favorite.objects.filter(user=user, toys=toys).delete()
    else:
        Favorite.objects.create(user=user, toys=toys)
    return Response("added to favorite", 200)

class FavoriteViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def filter_queryset(self, queryset):
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset
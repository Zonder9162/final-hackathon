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

from .models import Toy, Category, Comment, Like, Rating
from .serializers import ToySerializer, CategorySerializer, CommentSerializer
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
        queryset = sorted(self.get_queryset(), key=lambda toy: toy.average_rating, reverse=True)
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
    toy = get_object_or_404(Toy, id=t_id)

    if Like.objects.filter(user=user,toy=toy).exists():
        Like.objects.filter(user=user, toy=toy).delete()
    else:
        Like.objects.create(user=user, toy=toy)
    return Response("Like toggled", 200)

@api_view(['POST'])
def add_rating(request, a_id):
    user = request.user
    toy = get_object_or_404(Toy, id=t_id)
    value = request.POST.get('value')

    if not user.is_authenticated:
        raise ValueError("Authentication credentials are not provided")

    if not value:
        raise ValueError("Value is required")

    if Rating.objects.filter(user=user, toy=toy).exists():
        rating = Rating.objects.get(user=user, toy=toy)
        rating.value = value
        rating.save()
    else:
        Rating.objects.create(user=user,toy=toy, value=value)

    return Response('Rating created', 201)
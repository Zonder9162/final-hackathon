from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import ToyViewSet, CategoryViewSet, FavoriteViewSet, CommentViewSet, toggle_like, add_rating, add_to_favorite
from . import views 


router = DefaultRouter()
router.register('toys', ToyViewSet)
router.register('categories', CategoryViewSet)
router.register('comments', CommentViewSet)
# router.register('favorite', FavoriteViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('toys/toggle_like/<int:a_id>/', toggle_like),
    path('toys/add_rating/<int:a_id>/', add_rating),
    path('toys/add_to_favorite/<int:t_id>/', add_to_favorite),
  
]

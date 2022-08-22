from django.contrib import admin

from .models import Category, Toy, Like, Rating, Comment

admin.site.register(Category)
admin.site.register(Toy)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Comment)
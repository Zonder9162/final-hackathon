from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100)


class Toy(models.Model):
    categories = models.ManyToManyField(Category, related_name='toys')
    name = models.CharField(max_length=50)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media", null=True)

    @property
    def average_rating(self):
        ratings = [rating.value for rating in self.ratings.all()]
        if ratings:
            return sum(ratings) / len(ratings)
        return 0


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    product = models.ForeignKey(Toy, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    product = models.ForeignKey(Toy, related_name='comments', on_delete=models.CASCADE)    
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    product = models.ForeignKey(Toy, related_name='likes', on_delete=models.CASCADE)

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorite', on_delete=models.CASCADE)
    anime = models.ForeignKey(Toy, related_name='favorite', on_delete=models.CASCADE)
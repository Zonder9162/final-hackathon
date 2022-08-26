from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    value = models.CharField(max_length=1000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='chat')
    

    def __str__(self):
        return f'{self.user} -> {self.value}'
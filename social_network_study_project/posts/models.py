from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

#модель сообщества
class Group(models.Model):
    #имя сообщества
    title = models.CharField(max_length = 50, primary_key=True)
    #уникальный адрес группы, часть УРЫЛ
    slug = models.SlugField(unique = True)
    description = models.TextField()
    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
        )
    group = models.ForeignKey(
        Group,
        on_delete = models.SET_NULL, 
        blank=True, 
        null = True,
        related_name="posts"
        )
    def __str__(self):
        return self.text
    



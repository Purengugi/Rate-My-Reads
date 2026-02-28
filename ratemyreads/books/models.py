from django.db import models
from user_auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, default="")
    rating = models.FloatField()
    genre = models.CharField(max_length=100, default="")
    review = models.TextField(default="")
    published_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name='books')

    def __str__(self):
        return f"{self.title}: {self.rating}"


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
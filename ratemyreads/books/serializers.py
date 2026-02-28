from rest_framework import serializers
from .models import Book, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'user', 'book', 'created_at', 'updated_at']

class BookSerializer(serializers.ModelSerializer):
    users = 'user_auth.serializers.UserSerializer(many=True, read_only=True)'
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'rating', 'genre', 'review', 'published_date', 'users', 'comments']

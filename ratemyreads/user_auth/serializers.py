from rest_framework import serializers
from .models import User
from books.serializers import BookSerializer


class UserSerializer(serializers.ModelSerializer):
    # books = 'books.serializers.BooksSerializer(many=True, read_only=True)'
    books = BookSerializer(many=True, read_only=True)

    
    class Meta:
        model = User
        fields = ['email', 'name', 'is_active', 'is_superuser', 'is_staff', 'password', 'date_joined', 'last_login', 'books']
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
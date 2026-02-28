from rest_framework import generics
from .serializers import BookSerializer, CommentSerializer
from rest_framework import filters
from django.db.models import Avg
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Book, Comment
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'rating', 'published_date']
    permission_classes = [IsAuthenticated]


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        comment = serializer.save()

        # Send email notification to the current user
        if self.request.user.is_authenticated and self.request.user.id != comment.user.id: # Check if the current user is not the author of the comment
            subject = 'New Comment Notification'
            context = {'comment': comment}
            html_message = render_to_string('comment_notification_email.html', context)
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_email = self.request.user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        return comment



class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        # Send email notification to the current user if the comment is updated
        if self.request.user.id != instance.user:  # Check if the current user is not the author of the comment
            subject = 'Comment Updated Notification'
            context = {'comment': instance}
            html_message = render_to_string('comment_notification_email.html', context)
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_email = self.request.user.email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

    

class AverageRatingView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        average_rating = Book.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return Response({'average_rating': average_rating})

class TopRatedBooksView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.order_by('-rating')[:5]


class RecentlyAddedBooksView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        threshold_date = timezone.now() - timezone.timedelta(weeks=1)
        return Book.objects.filter(published_date__gte=threshold_date)
    

class BooksByGenreAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        # Retrieve the genre from the query parameters
        genre = self.kwargs.get('genre')

        # Filter books by genre
        queryset = Book.objects.filter(genre=genre)
        return queryset
from django.urls import path, include
from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView, AverageRatingView, TopRatedBooksView, RecentlyAddedBooksView, BooksByGenreAPIView, CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    path('books/average_rating/', AverageRatingView.as_view(), name='average_rating'),
    path('books/top_rated/', TopRatedBooksView.as_view(), name="top_rated"),
    path('books/recently_added/', RecentlyAddedBooksView.as_view(), name="recently_added"),
    path('books/genre/<str:genre>/', BooksByGenreAPIView.as_view(), name="genre"),
]

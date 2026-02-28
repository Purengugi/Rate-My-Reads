from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView, BooksByGenreAPIView
from django.utils import timezone
from .models import Book, Comment
from user_auth.models import User
from .serializers import BookSerializer, CommentSerializer


class BookViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.regular_user = User.objects.create_user(email="firstuser@mail.com", name="firstuser",
                            is_active=True, is_staff=False, is_superuser=False,
                            password="firstuserpass")
        self.client.force_authenticate(user=self.regular_user)
        self.book1 = Book.objects.create(title="Book 1", rating=5, published_date="2024-01-01")
        self.book2 = Book.objects.create(title="Book 2", rating=4, published_date="2024-02-01")

    def test_list_books(self):
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book(self):
        book_data = {
        "title": "New Book",
        "rating": 3,
        "published_date": "2024-03-01",
        "users": [self.regular_user.id]
        }
        response = self.client.post(reverse('book-list-create'), book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(title="New Book").rating, 3)
    
    def test_book_retrieve_update_destroy_api_view(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'title': 'Updated Book', 'rating': '3.4', 'users': [self.regular_user.id] }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=self.book1.pk).title, 'Updated Book')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_average_rating_view(self):
        url = reverse('average_rating')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('average_rating', response.data)

    def test_top_rated_books_view(self):
        url = reverse('top_rated')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming only 2 books are created in setUp

    def test_recently_added_books_view(self):
        url = reverse('recently_added')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that no books are returned initially since no books are added recently
        self.assertEqual(len(response.data), 2)

        # Add a new book and check if it appears in the recently added books view
        Book.objects.create(title="Newly Added Book", rating=4.2)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 3)

    def test_books_by_genre_api_view(self):
        url = reverse('genre', kwargs={'genre': 'fiction'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure that only books with the specified genre are returned
        for book in response.data:
            self.assertEqual(book['genre'], 'fiction')


class CommentViewsTestCase(TestCase):
    def setUp(self):
        # Create a regular user for authentication
        self.regular_user = User.objects.create_user(email="regularuser@mail.com", name="Regular User",
                                                      is_active=True, is_staff=False, is_superuser=False,
                                                      password="regularuserpass")
        self.book1 = Book.objects.create(title="Book 1", rating=5, published_date="2024-01-01")
        self.book2 = Book.objects.create(title="Book 2", rating=4, published_date="2024-02-01")

        # Authenticate the client with the regular user
        # self.client.force_authenticate(user=self.regular_user)

        # Create some comments for testing
        self.comment1 = Comment.objects.create(text="Comment 1", user=self.regular_user, book=self.book1)
        self.comment2 = Comment.objects.create(text="Comment 2", user=self.regular_user, book=self.book2)

    def test_list_comments(self):
        url = reverse('comment-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_comment(self):
        url = reverse('comment-list-create')
        comment_data = {
            "text": "New Comment",
            "user": [self.regular_user.id],
            "book": self.book1.id
        }
        response = self.client.post(url, comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 3)
        self.assertEqual(Comment.objects.get(text="New Comment").user, self.regular_user)

    def test_comment_retrieve_update_destroy_api_view(self):
        url = reverse('comment-detail', kwargs={'pk': self.comment1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'text': 'Updated Comment', 'user': self.regular_user.id, 'book': self.book2.id}
        response = self.client.put(url, data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(pk=self.comment1.pk).text, 'Updated Comment')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment1.pk).exists())
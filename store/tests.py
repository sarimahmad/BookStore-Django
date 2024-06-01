from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Category, Book, Cart, Purchase
from accounts.models import StoreUser


class StoreTests(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'username': 'testuser'
        }
        self.user = StoreUser.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

        self.author = Author.objects.create(user=self.user, name="Author 1")
        self.category = Category.objects.create(user=self.user, name="Category 1")
        self.book = Book.objects.create(
            user=self.user,
            title="Book 1",
            author=self.author,
            category=self.category,
            price=100
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart.books.add(self.book)
        self.purchase_url = reverse('purchases-list')
        self.book_url = reverse('books-list')

    def test_create_book(self):
        data = {
            'title': 'Book 2',
            'author': self.author.id,
            'category': self.category.id,
            'price': 150
        }
        response = self.client.post(self.book_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Book 2')

    def test_get_books(self):
        response = self.client.get(self.book_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book 1')

    def test_update_book(self):
        data = {
            'title': 'Updated Book Title',
            'price': 200
        }
        book_detail_url = reverse('books-detail', kwargs={'pk': self.book.id})
        response = self.client.patch(book_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book Title')
        self.assertEqual(response.data['price'], 200)

    def test_delete_book(self):
        book_detail_url = reverse('books-detail', kwargs={'pk': self.book.id})
        response = self.client.delete(book_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_create_purchase(self):
        data = {
            'total_amount': 100
        }
        response = self.client.post(self.purchase_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_amount'], 100)
        self.assertEqual(len(response.data['items']), 1)

    def test_get_purchases(self):
        data = {
            'total_amount': 100
        }
        self.client.post(self.purchase_url, data, format='json')
        response = self.client.get(self.purchase_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['total_amount'], 100)

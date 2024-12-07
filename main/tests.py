from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from main.models import Book


class BookAPITests(APITestCase):

    def setUp(self):
        # Створення користувачів для аутентифікації
        self.user = User.objects.create_user(username='test user', password='test password')
        self.admin_user = User.objects.create_superuser(username='admin user', password='admin password')

        # Створення книги
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            genre='Fiction',
            publication_year=2023
        )

    def test_create(self):
        #Тест на додавання нової книги"""
        self.client.login(username='test user', password='test password')
        url = '/api/books/'
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'genre': 'Science',
            'publication_year': 2024
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(response.data['author'], 'New Author')

    def test_list(self):
        # тест на отримання списку всіх книг"""
        url = '/api/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Book', str(response.data))  # Перевіряємо, що тестова книга є в списку

    def test_get(self):
        # тест на перегляд деталей окремої книги
        url = f'/api/books/{self.book.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['author'], 'Test Author')

    def test_update(self):
        # тест на оновлення інформації про книгу
        self.client.login(username='test user', password='test password')
        url = f'/api/books/{self.book.id}/'
        data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'genre': 'Drama',
            'publication_year': 2025
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')
        self.assertEqual(response.data['author'], 'Updated Author')

    def test_delete(self):
        # тест на видалення книги (тільки адміністратор)
        self.client.login(username='admin user', password='admin password')
        url = f'/api/books/{self.book.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


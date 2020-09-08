from django.test import TestCase, Client
from .models import Book

# Create your tests here.


class BookTestCase(TestCase):
    fixtures = ['db.json']

    def test_get_books(self):
        books = Book.objects.all()
        self.assertEqual(books.count() > 0, True)


class BookViewsTestCase(TestCase):
    def test_can_display_books(self):
        c = Client()
        response = c.get('/books/')
        self.assertEqual(response.status_code, 200)

from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from books.models import Book
from .models import Purchase

# Create your tests here.


class CheckoutTestCase(TestCase):
    fixtures = ['db.json']

    def test_can_calculate_total(self):
        # find the book with book_id 1
        book = get_object_or_404(Book, pk=1)
        user = get_object_or_404(User, pk=1)
        purchase = Purchase()
        purchase.book = book
        purchase.user = user
        purchase.price = book.cost
        purchase.qty = 2
        purchase.save()

        self.assertAlmostEqual(purchase.total, 2 * book.cost)

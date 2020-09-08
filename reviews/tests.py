from django.test import TestCase
from django.shortcuts import get_object_or_404
from .models import Review
from books.models import Book
from django.contrib.auth.models import User
from django.test import Client
import datetime


# Create your tests here.
class ReviewTestCase(TestCase):
    fixtures = ['db.json']

    # def test_get_reviews(self):
    #     reviews = Review.objects.all()
    #     # self.assertEqual(reviews.count() > 0, True)
    #     self.assertGreater(reviews.count(), 1000)

    def test_create_review(self):
        book = get_object_or_404(Book, pk=1)
        author = get_object_or_404(User, pk=1)

        review = Review()
        review.title = "Test review"
        review.content = "test content"
        review.date = datetime.date.today()
        review.book = book
        review.author = author

        review.save()

        test_review = get_object_or_404(Review, pk=review.id)
        self.assertEqual(test_review.title, "Test review")
        self.assertEqual(test_review.content, "test content")
        self.assertEqual(test_review.date, datetime.date.today())
        self.assertEqual(test_review.book, book)
        self.assertEqual(test_review.author, author)


class ReviewRouteTestCase(TestCase):
    fixtures = ["db.json"]

    def test_can_view_reviews(self):
        c = Client()
        response = c.get('/reviews/')
        self.assertEqual(response.status_code, 200)

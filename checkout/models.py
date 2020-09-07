from django.db import models

from books.models import Book
from django.contrib.auth.models import User

# Create your models here.


class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now=True)
    qty = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"Purchase made for id:{self.book.id} by {self.user.username}" \
            f" on {self.purchase_date}"

    # override the default save
    def save(self, *args, **kwargs):
        self.total = self.price * self.qty
        super().save(*args, **kwargs)

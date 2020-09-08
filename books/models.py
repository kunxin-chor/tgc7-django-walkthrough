from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.


class Genre(models.Model):
    title = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(blank=False, max_length=255, unique=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    # what are the "columns" inside the Book table
    title = models.CharField(blank=False, max_length=255)
    ISBN = models.CharField(blank=False, max_length=255)
    desc = models.TextField(blank=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author')
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    page_count = models.IntegerField(blank=False)
    cover = CloudinaryField()
    cost = models.DecimalField(max_digits=10, decimal_places=3, blank=False)

    # to-string
    def __str__(self):
        return self.title + " - " + self.ISBN


class Publisher(models.Model):
    # what are the columns (aka. fields) inside the Publisher table
    name = models.CharField(blank=False, max_length=255, unique=True)
    email = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(blank=False, max_length=100)
    last_name = models.CharField(blank=False, max_length=100)
    dob = models.DateField(blank=False)
    email = models.CharField(blank=False, max_length=100, unique=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

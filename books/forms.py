from django import forms
from .models import Book, Publisher, Author, Genre, Tag
from cloudinary.forms import CloudinaryJsFileField
from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('owner',)
    cover = CloudinaryJsFileField()

    def clean_ISBN(self):
        # extract out the data to be cleaned
        data = self.cleaned_data['ISBN']

        # check if the ISBN already exists
        books = Book.objects.filter(ISBN=data)
        if books.count() > 0:
            raise ValidationError("The ISBN is not unique!")

        return data


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ('name', 'email')


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class SearchForm(forms.Form):
    search_terms = forms.CharField(max_length=100, required=False)
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False
    )

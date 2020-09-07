from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from .models import Book, Publisher, Author
from .forms import BookForm, PublisherForm, AuthorForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
# Create your views here.


def index(request):
    # create a query set that has all the books
    # a query set is like a cursor

    # SELECT * FROM books
    # all_books = Book.objects.all()

    # SELECT * FROM books WHERE title = "The Lord of the Rings"
    # all_books = Book.objects.filter(title="Lord of the Rings")

    # SELECT * FROM books where genre_id = 1
    # all_books = Book.objects.filter(genre_id=1)

    # SELECT * FROM books where title LIKE "%lord%"
    # all_books = Book.objects.filter(title__icontains="Lord")

    # SELECT * FROM books where title LIKE '%lord%' AND genre_id=1
    # all_books = Book.objects.filter(
    #     title__icontains='Lord'
    # ).filter(
    #     genre_id=1
    # )

    # SELECT * from books join books_tags on books.id = books_tags.book_id
    # AND WHERE tag_id in (2)
    # all_books = Book.objects.filter(tags__in=[2])

    # SELECT * from books where page_count >= 100
    # all_books = Book.objects.filter(page_count__gte=100)

    # Using the Q Objects

    # select all the books with page count greater or equal to 100
    # AND must have the tag boring
    # query = Q(page_count__gte=100)
    # query = query and Q(tags__in=[2])

    # select all the books with page counter greater or equal to 100
    # OR have the tag boring
    # query = Q(page_count__gte=100)
    # query = query or Q(tags__in=[2])

    # select all the books with `lord` in the title OR (page count greater
    # than 100 and has the tag boring)

    # have_lord_in_title = Q(title__icontains='lord')
    # page_counter_greater_100 = Q(page_count__gt=100)
    # have_tag_boring = Q(tags__in=[2])

    # query = have_lord_in_title | (
    #     page_counter_greater_100 & have_tag_boring)

    # all_books = Book.objects.filter(query)

    search_form = SearchForm(request.GET)

    # create an empty Query object (i.e, always true)
    # in SQL, it is: SELECT * from book WHERE 1
    query = ~Q(pk__in=[])

    if request.GET:
        # get books that have the search terms in the title
        if 'search_terms' in request.GET and request.GET['search_terms']:
            query = query & Q(title__icontains=request.GET['search_terms'])

        if 'genre' in request.GET and request.GET['genre']:
            query = query & Q(genre=request.GET['genre'])

        if 'tags' in request.GET and request.GET['tags']:
            query = query & Q(tags__in=request.GET['tags'])

    all_books = Book.objects.filter(query)

    return render(request, "books/index.template.html", {
        'all_books': all_books,
        'search_form': search_form
    })


def success(request):
    return render(request, 'books/login_success.template.html')


def show_publisher(request):
    all_publishers = Publisher.objects.all()
    return render(request, "books/show_publishers.template.html", {
        'all_publishers': all_publishers
    })


def show_authors(request):
    all_authors = Author.objects.all()
    return render(request, "books/show_authors.template.html", {
        'all_authors': all_authors
    })


@login_required
def create_book(request):
    # if the user submits the data
    if request.method == "POST":
        # take whatever the user has submitted (stored inside
        # request.POST) and populate an instance of BookForm
        submitted_form = BookForm(request.POST)

        # test if the form is valid
        if submitted_form.is_valid():
            # when commit=False is there, it means
            # don't save to the database straightaway
            book_model = submitted_form.save(commit=False)
            book_model.owner = request.user
            # manually save the model to the database
            book_model.save()
            messages.success(
                request,
                f"New book {submitted_form.cleaned_data['title']} has been"
                " created")
            return redirect(reverse(index))
        else:
            return render(request, "books/create_book.template.html", {
                'form': submitted_form
            })
    else:
        # if user did not submit the data, just display the form
        create_book_form = BookForm()
        return render(request, "books/create_book.template.html", {
            'form': create_book_form
        })


def view_book_details(request, book_id):
    book_model = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_details.template.html', {
        "book": book_model
    })


def create_publisher(request):
    if request.method == "POST":
        # 1. create the form and populate it with the user's input
        submitted_form = PublisherForm(request.POST)
        if submitted_form.is_valid():
            # 2. if the submitted information is valid, save
            submitted_form.save()
            return redirect(reverse(show_publisher))

    else:
        publisher_form = PublisherForm()
        return render(request, 'books/create_publisher.template.html', {
            'form': publisher_form
        })


def create_author(request):
    if request.method == "POST":
        author_form = AuthorForm(request.POST)
        if author_form.is_valid():
            author_form.save()
            return redirect(reverse(show_authors))
    else:
        author_form = AuthorForm()
        return render(request, 'books/create_author.template.html', {
            'form': author_form
        })


def update_book(request, book_id):
    if request.method == "POST":
        # 1. retrieve the book that is being updated
        book_being_updated = get_object_or_404(Book, pk=book_id)

        # 2. do the modification
        book_form = BookForm(request.POST, instance=book_being_updated)

        # 3. save if the form is valid
        if book_form.is_valid():
            book_form.save()

            # 4. redirect
            return redirect(reverse(index))
    else:
        # 1. retrieve the book that we are editing
        book_being_updated = get_object_or_404(Book, pk=book_id)

        # 2. create the form containing the existing book's book data
        form = BookForm(instance=book_being_updated)

        # 3. display the form in a template
        return render(request, 'books/update_book.template.html', {
            'form': form
        })


# the second argument `book_id` is the id of the book
# that we want to delete
def delete_book(request, book_id):
    if request.method == "POST":
        book_to_delete = get_object_or_404(Book, pk=book_id)
        book_to_delete.delete()
        return redirect(reverse(index))
    else:
        # 1. fetch the book that we want to delete
        book_to_delete = get_object_or_404(Book, pk=book_id)

        # 2. ask for confirmation if we want to delete
        return render(request, 'books/delete_book.template.html', {
            'book': book_to_delete
        })

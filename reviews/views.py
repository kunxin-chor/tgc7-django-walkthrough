from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from books.models import Book
from .models import Review
from .forms import ReviewForm, SearchReviewForm

# Create your views here.


def index(request):

    form = SearchReviewForm(request.GET)

    # create the always true query
    # the following means `WHERE 1` in SQL
    query = ~Q(pk__in=[])

    if request.GET:
        # to search by the review title
        if 'review_title' in request.GET and request.GET['review_title']:
            review_title = request.GET['review_title']
            query = query & Q(title__icontains=review_title)

        # to search by book title
        if 'book_title' in request.GET and request.GET['book_title']:
            query = query & Q(book__title__icontains=request.GET['book_title'])

        # search by author
        if 'author' in request.GET and request.GET['author']:
            query = query & Q(author=request.GET['author'])

    all_reviews = Review.objects.filter(query)

    return render(request, 'reviews/show_reviews.template.html', {
        'all_reviews': all_reviews,
        'form': form
    })


@login_required
def create(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_model = form.save(commit=False)
            review_model.book = book
            review_model.author = request.user
            review_model.save()
            messages.success(request, "New review added successfully!")
            return redirect(reverse('book_details_route', kwargs={'book_id': book_id}))
    else:
        form = ReviewForm()
        return render(request, 'reviews/create.template.html', {
            'form': form,
            'book': book
        })

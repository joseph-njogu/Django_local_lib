
from django.shortcuts import render

# # from django.shortcuts import get_object_or_404
# from django.http import HttpResponseRedirect
# from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book, Author, BookInstance
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
   # # Available copies of books
    num_instances_available = \
        BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    # num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html
    # with the data in the context variable.
    return render(request,'index.html',context={
                                                'num_books': num_books,
                                                'num_instances': num_instances,
                                                'num_instances_available': num_instances_available,
                                                'num_authors': num_authors, }
    )


class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 2


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 2


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author

@permission_required('catalog.can_mark_returned')
class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    # Generic class-based view listing all books
    # on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 2


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


# Classes created for the forms challenge
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'

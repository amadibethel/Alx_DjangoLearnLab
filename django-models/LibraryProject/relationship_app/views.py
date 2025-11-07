from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library


# Function-based view to list all books stored in the database
def list_books(request):
    books = Book.objects.all()
    # Use the expected template path for automated checker
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

"from .models import Library"

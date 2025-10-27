# Retrieve Book records

from bookshelf.models import Book
# Get all books
books = Book.objects.all()

# Get a single book by id
book = Book.objects.get(id=1)

# Filter books by author
books_by_author = Book.objects.filter(author="F. Scott Fitzgerald")


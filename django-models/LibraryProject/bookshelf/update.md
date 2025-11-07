# Update a Book record

from bookshelf.models import Book
book = Book.objects.get(id=1)
book.title = "The Great Gatsby (Updated Edition)"
book.save()

Nineteen Eighty-Four
